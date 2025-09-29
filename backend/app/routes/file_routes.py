# routes/file_routes.py
from flask import Blueprint, request, jsonify
from ..services.file_service import upload_service, transform_service
from ..services.database_service import DatabaseService 

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
    
    # Step 2: Transform and save successful files
    transform_results = {}
    database_results = {}
    
    for result, file in zip(upload_results, files):
        if result["status"] == "Success":
            try:
                # Transform the data (now creates SQLAlchemy models directly)
                file_transform_result = transform_service([file], upload_results, result["schema"])
                transform_results.update(file_transform_result)
                
                # Step 3: Save to database
                db_result = DatabaseService.save_records_by_file(
                    file_transform_result, 
                    use_bulk=False  # Set to True for better performance, False for full validation
                )
                database_results.update(db_result)
                
            except Exception as e:
                # Handle any transformation errors
                database_results[file.filename] = {
                    "success": False,
                    "message": f"Processing error: {str(e)}",
                    "count": 0
                }

    # Step 4: Prepare comprehensive response
    final_results = []
    total_records_saved = 0
    successful_saves = 0
    
    for i, result in enumerate(upload_results):
        filename = files[i].filename
        
        final_result = {
            "file": filename,
            "upload_status": result["status"],
            "schema": result.get("schema"),
            "missing_columns": result.get("missing_columns"),
            "extra_columns": result.get("extra_columns")
        }
        
        # Add database save results if available
        if filename in database_results:
            db_result = database_results[filename]
            final_result.update({
                "database_save_success": db_result["success"],
                "records_saved": db_result["count"],
                "database_message": db_result["message"]
            })
            
            if db_result["success"]:
                total_records_saved += db_result["count"]
                successful_saves += 1
        else:
            # File upload failed, so no database operation attempted
            final_result.update({
                "database_save_success": False,
                "records_saved": 0,
                "database_message": "File upload failed"
            })
        
        final_results.append(final_result)

    return jsonify({
        "success": len([r for r in final_results if r["database_save_success"]]) > 0,
        "results": final_results,
        "summary": {
            "total_files": len(files),
            "successful_uploads": len([r for r in upload_results if r["status"] == "Success"]),
            "successful_database_saves": successful_saves,
            "total_records_saved": total_records_saved,
            "failed_files": [r["file"] for r in final_results if not r["database_save_success"]]
        }
    })
