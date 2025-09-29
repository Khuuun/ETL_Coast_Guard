# routes/file_routes.py
from flask import Blueprint, request, jsonify
from ..services.file_service import upload_service, transform_service
from ..services.database_service import DatabaseService 
from ..models.file_model import AuditRecord, OJTLog

file_bp = Blueprint("file_bp", __name__)

# Your existing SCHEMA definition stays the same
SCHEMA = {
    "AuditRecords": [
        "CALENDAR YEAR",
        "AS OF", 
        "AOM NO.",
        "AUDIT TYPE",
        "AUDIT OBSERVATION",
        "AUDIT OBSERVATION DESCRIPTION",
        "AUDIT RECOMMENDATIONS",
        "AGENCY ACTION PLAN",
        "PERSON/ DEPARTMENT RESPONSIBLE",
        "TARGET IMPLEMENTATION FROM",
        "TARGET IMPLEMENTATION TO",
        "MANAGEMENT'S COMMENT",
        "AUDITOR'S REJOINDER",
        "ACTIONS TO BE TAKEN",
        "CONSOLIDATED BY",
        "NOTED BY"
    ],
    "OJT_Logs": [
        "Employee ID",
        "Department", 
        "Employee Name",
        "Time",
        "Date",
        "Activity",
        "Image",
        "Address"
    ]
}

@file_bp.route("/upload", methods=["POST"])
def upload_files():
    if "files" not in request.files:
        return jsonify({"error": "No files part in request"}), 400

    files = request.files.getlist("files")
    
    # Step 1: Validate file structure
    upload_results = upload_service(files, SCHEMA)
    
    # Step 2: Transform files but DO NOT save to DB yet. Return transformed records for frontend confirmation.
    transform_results = {}

    for result, file in zip(upload_results, files):
        if result.get("status") == "Success":
            try:
                file_transform_result = transform_service([file], upload_results, result.get("schema"))
                transform_results.update(file_transform_result)
            except Exception as e:
                transform_results[file.filename] = {"error": str(e)}
        else:
            transform_results[file.filename] = {"error": "Upload failed or structure mismatch"}

    # Prepare response containing upload metadata and transformed payload (not saved)
    final_results = []
    for i, result in enumerate(upload_results):
        filename = files[i].filename
        fr = {
            "file": filename,
            "upload_status": result.get("status"),
            "schema": result.get("schema"),
            "missing_columns": result.get("missing_columns"),
            "extra_columns": result.get("extra_columns"),
            "transformed_preview_count": len(transform_results.get(filename, [])) if isinstance(transform_results.get(filename), list) else 0
        }
        final_results.append(fr)

    return jsonify({
        "success": True,
        "results": final_results,
        "transformed": transform_results,
        "summary": {
            "total_files": len(files),
            "successful_uploads": len([r for r in upload_results if r["status"] == "Success"]),
        }
    })


@file_bp.route("/save", methods=["POST"])
def save_transformed():
    """Accept transformed records (JSON) and persist to the database.

    Expected payload:
    {
      "files": { "filename.csv": [ {..record..}, ... ], ... },
      "use_bulk": false
    }
    """
    payload = request.get_json() or {}
    files_payload = payload.get("files") or {}
    use_bulk = payload.get("use_bulk", False)

    # Convert plain dicts into model instances grouped per file
    records_per_file = {}
    for filename, records in files_payload.items():
        if not records:
            records_per_file[filename] = {"error": "No records provided"}
            continue

        model_instances = []
        # Determine schema by inspecting keys of first record
        first = records[0]
        if "aom_no" in first and "as_of" in first:
            # AuditRecords
            for r in records:
                model_instances.append(AuditRecord(
                    calendar_year=r.get("calendar_year"),
                    as_of=r.get("as_of"),
                    aom_no=r.get("aom_no"),
                    audit_type=r.get("audit_type"),
                    audit_observation=r.get("audit_observation"),
                    audit_observation_description=r.get("audit_observation_description"),
                    audit_recommendations=r.get("audit_recommendations"),
                    agency_action_plan=r.get("agency_action_plan"),
                    person_or_department_responsible=r.get("person_or_department_responsible"),
                    target_implementation_from=r.get("target_implementation_from"),
                    target_implementation_to=r.get("target_implementation_to"),
                    management_comment=r.get("management_comment"),
                    auditors_rejoinder=r.get("auditors_rejoinder"),
                    actions_to_be_taken=r.get("actions_to_be_taken"),
                    consolidated_by=r.get("consolidated_by"),
                    noted_by=r.get("noted_by"),
                ))
        elif "employee_id" in first and "activity" in first:
            for r in records:
                model_instances.append(OJTLog(
                    employee_id=r.get("employee_id"),
                    department=r.get("department"),
                    employee_name=r.get("employee_name"),
                    time=r.get("time"),
                    date=r.get("date"),
                    activity=r.get("activity"),
                    image=r.get("image"),
                    address=r.get("address"),
                ))
        else:
            records_per_file[filename] = {"error": "Unknown record shape"}
            continue

        records_per_file[filename] = model_instances

    # Use DatabaseService to save grouped records
    save_results = DatabaseService.save_records_by_file(records_per_file, use_bulk=use_bulk)

    return jsonify({"success": True, "results": save_results})
