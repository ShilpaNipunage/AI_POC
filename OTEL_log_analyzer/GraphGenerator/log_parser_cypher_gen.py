import json
from typing import Iterator, Dict, Any, List, Optional
import re


def _extract_attributes(attributes_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Helper to extract key-value pairs from OTEL attributes list."""
    return {attr['key']: attr['value']['stringValue'] for attr in attributes_list if 'stringValue' in attr['value']}

def process_resource_log_data(resource_log_unit: Dict[str, Any]) -> List[str]:
    """
    Processes a single 'resourceLog' dictionary from the OTEL export format.
    It extracts data from all contained 'scopeLogs' and 'logRecords'.
    """
    print("ENTER process_resource_log_data...")
    final_cypher_query_list = []
    resource_attrs = _extract_attributes(resource_log_unit.get("resource", {}).get("attributes", []))
    service_name = resource_attrs.get("service.name")
    service_version = resource_attrs.get("service.version", "")
    service_instance = resource_attrs.get("service.instance.id", "")


    if not service_name:
        print("Warning: Skipping resourceLog unit with no service.name. \nresource_attrs:{resource_attrs}")
        return []
    
    service_query = f"""
MERGE (s:Service {{name: '{service_name}', version: '{service_version}', instance: '{service_instance}'}})
"""
    cypher_query = service_query + f"""
SET s.attributes = '{json.dumps(resource_attrs)}'
"""
    cypher_query.strip()
    
    # print(f"\n\nAdding to final_cypher_query_list: {cypher_query}")
    final_cypher_query_list.append(cypher_query)
    
    print(f"\nNo. of scopeLogs in resource_log_unit: {len(resource_log_unit.get('scopeLogs', []))}")

    for scope_log in resource_log_unit.get("scopeLogs", []):
        ## NOTE : If there are no logRecords, the empty scope will not be created.
        scope_name = scope_log.get("scope", {}).get("name", "")
        scope_query = f"""
MERGE (sc:Scope {{name: '{scope_name}'}})
MERGE (s)-[:HAS_SCOPE]->(sc)
"""
        logRecords = scope_log.get("logRecords", [])
        final_cypher_query_list = processScopeLogRecords(final_cypher_query_list, service_query, scope_query, logRecords)

    # print(f"\n\n\n resource_log:{resource_log_unit}\n\n final_cypher_query_list:{final_cypher_query_list}")

    print("EXIT process_resource_log_data...")

    return final_cypher_query_list

def processScopeLogRecords(final_cypher_query_list, service_query, scope_query, logRecords):
    print(f"\nNo. of logRecords in scope_log: {len(logRecords)}")

    for record in logRecords:
        final_cypher_query = ""
        cypher_query = service_query + scope_query
        cypher_query.strip()
        final_cypher_query = final_cypher_query + cypher_query
        final_cypher_query = processLogRecord(final_cypher_query, record)
        final_cypher_query_list.append(final_cypher_query)

    return final_cypher_query_list

def processLogRecord(final_cypher_query, record):
    body_value = record.get("body", {}).get("stringValue", "")

    trace_id = record.get("traceId", "")
    if not trace_id:
        trace_id = "EMPTY_TRACE"
        
    span_id = record.get("spanId", "")
    if not span_id:
        span_id = "EMPTY_SPAN"

    cypher_query = f"""
MERGE (op:Operation {{name: {json.dumps(body_value)}}})
MERGE (sc)-[r:MADE_OPERATION]->(op)
SET r.timestamp_unix_nano = {record.get("timeUnixNano", 0)},
    r.observed_timestamp_unix_nano = {record.get("observedTimeUnixNano", 0)},
    r.severity_number = {record.get("severityNumber", 0)},
    r.severity_text = '{record.get("severityText", "")}'
MERGE (t:Trace {{trace_id: '{trace_id}'}})
MERGE (sp:Span {{span_id: '{span_id}'}})
MERGE (sc)-[:IN_TRACE]-> (t)
MERGE (t)-[:HAS_SPAN]->(sp)
MERGE(t)-[:HAS_SERVICE]->(s)
            """

    cypher_query.strip()
    final_cypher_query = final_cypher_query + cypher_query
            
    parent_span_id = record.get("parentSpanId", "")

    if parent_span_id:
        cypher_query = f"""
MERGE (parent:Span {{span_id : parent_span_id}})
MERGE (parent)-[:HAS_CHILD]->(sp)
"""
        cypher_query.strip()
        final_cypher_query = final_cypher_query + cypher_query

    return final_cypher_query


def read_logs_from_file(file_path: str) -> Iterator[Dict[str, Any]]:
    """
    Reads log data from a file where each line is expected to be a complete JSON object.
    It attempts to convert Python-like string literals within each line to valid JSON before parsing.
    It yields each complete 'resourceLog' dictionary found in the file.
    """

    # import os
    # print("Current working dir:", os.getcwd())

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip() # Remove leading/trailing whitespace including newline
                if not line:
                    continue # Skip empty lines

                try:
                    obj = json.loads(line)
                    
                    if isinstance(obj, dict) and "resourceLogs" in obj:
                        # The decoded 'obj' is expected to be a top-level OTEL log unit
                        # (e.g., {'resourceLogs': [...]}). We need to yield each individual
                        # resourceLog dictionary from within its 'resourceLogs' array.
                        for resource_log_item in obj.get("resourceLogs", []):
                            yield resource_log_item
                    else:
                        print(f"Warning: Line {line_num} does not contain 'resourceLogs' key as expected, or is not a dictionary. Skipping.")
                        
                except json.JSONDecodeError as e:
                    print(f"Warning: JSONDecodeError on line {line_num}: {e}. Content starts with: {line[:200]}... Skipping line.")
                except Exception as e:
                    print(f"An unexpected error occurred while processing line {line_num}: {e}. Content starts with: {line[:200]}... Skipping line.")

    except FileNotFoundError:
        print(f"Error: Log file not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the log file: {e}")