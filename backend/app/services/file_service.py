import pandas as pd
from ..models.file_model import AuditRecord, OJTLog
import re

def read_file_with_multiple_encodings(f):
    encodings_to_try = ["utf-8-sig", "cp1252", "latin1"]
    for enc in encodings_to_try:
        try:
            f.seek(0)  # reset pointer
            return pd.read_csv(
                f,
                encoding=enc,
                quotechar='"',
                escapechar='\\',
                on_bad_lines='skip'
            )
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Could not decode file with supported encodings")



def upload_service(files, SCHEMA):
    results = []

    def normalize(col):
        col = str(col).strip()
        col = col.encode('utf-8').decode('utf-8-sig')
        col = re.sub(r'\s+', '', col)
        col = col.lower()
        col = col.replace("’", "'")
        return col  


    for f in files:
        try:
            if f.filename.endswith(".csv"):
                df = read_file_with_multiple_encodings(f)
            elif f.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(f)
            else:
                results.append({"file": f.filename, "status": "Unsupported file type"})
                continue

            file_cols_original = list(df.columns)
            file_cols_norm_map = {normalize(c): c for c in file_cols_original}
            file_cols_norm = set(file_cols_norm_map.keys())

            best_match = None
            for schema_name, expected_cols in SCHEMA.items():
                expected_cols_norm_map = {normalize(c): c for c in expected_cols}
                expected_cols_norm = set(expected_cols_norm_map.keys())

                missing_norm = expected_cols_norm - file_cols_norm
                extra_norm = file_cols_norm - expected_cols_norm

                if not missing_norm and not extra_norm:
                    # perfect match
                    best_match = {
                        "schema": schema_name,
                        "missing_columns": None,
                        "extra_columns": None
                    }
                    break
                else:
                    # store mismatch info but still continue
                    best_match = {
                        "schema": schema_name,
                        "missing_columns": [expected_cols_norm_map[n] for n in missing_norm],
                        "extra_columns": [file_cols_norm_map[n] for n in extra_norm]
                    }

            # after trying all schemas
            results.append({
                "file": f.filename,
                "schema": best_match["schema"],
                "status": "Success" if not best_match["missing_columns"] and not best_match["extra_columns"]
                          else "File Structure Mismatch",
                "missing_columns": best_match["missing_columns"],
                "extra_columns": best_match["extra_columns"]
            })

        except Exception as e:
            results.append({"file": f.filename, "status": "Failed", "error": str(e)})

    return results



def transform_service(files, results, schema):
    records_per_file = {}
    for f in files:
        file_records = []
        try:
            f.seek(0)
            
            df = read_file_with_multiple_encodings(f)

            if df is None:
                records_per_file[f.filename] = {"error": "Could not decode file with supported encodings"}
                continue

            if df.empty:
                records_per_file[f.filename] = {"error": "File is empty"}
                continue

            # Convert NaN → None
            df = df.where(pd.notnull(df), None)

            # Build AuditRecord objects
            if schema == "AuditRecords":
                df.columns = [c.strip().upper() for c in df.columns]

                for i, row in df.iterrows():
                    record = AuditRecord(
                        calendar_year=row.get("CALENDAR YEAR"),
                        as_of=row.get("AS OF"),
                        aom_no=row.get("AOM NO."),
                        audit_type=row.get("AUDIT TYPE"),
                        audit_observation=row.get("AUDIT OBSERVATION"), 
                        audit_observation_description=row.get("AUDIT OBSERVATION DESCRIPTION"),
                        audit_recommendations=row.get("AUDIT RECOMMENDATIONS"), 
                        agency_action_plan=row.get("AGENCY ACTION PLAN"),
                        person_or_department_responsible=row.get("PERSON/ DEPARTMENT RESPONSIBLE"), 
                        target_implementation_from=row.get("TARGET IMPLEMENTATION FROM"),
                        target_implementation_to=row.get("TARGET IMPLEMENTATION TO"), 
                        management_comment=row.get("MANAGEMENT’S COMMENT"), 
                        auditors_rejoinder=row.get("AUDITOR’S REJOINDER"),
                        actions_to_be_taken=row.get("ACTIONS TO BE TAKEN"), 
                        consolidated_by=row.get("CONSOLIDATED BY"), 
                        noted_by=row.get("NOTED BY")
                    )
                    file_records.append(record)
            elif schema == "OJT_Logs":
                df.columns = [c.strip().upper() for c in df.columns]
                for i, row in df.iterrows():
                    record = OJTLog(
                        employee_id=str(row.get("EMPLOYEE ID")) if row.get("EMPLOYEE ID") is not None else None,
                        department=row.get("DEPARTMENT"),
                        employee_name=row.get("EMPLOYEE NAME"),
                        time=row.get("TIME"),
                        date=str(row.get("DATE")) if row.get("DATE") is not None else None,
                        activity=str(row.get("ACTIVITY")) if row.get("ACTIVITY") is not None else None,
                        image=row.get("IMAGE"),
                        address=row.get("ADDRESS")
                    )
                    file_records.append(record)


            records_per_file[f.filename] = file_records

        except Exception as e:
            records_per_file[f.filename] = {"error": str(e)}

    return records_per_file


