# services/database_service.py
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from ..models.file_model import AuditRecord, OJTLog
from .. import db


class DatabaseService:
    """Service for saving SQLAlchemy records with or without bulk insert."""

    @staticmethod
    def _handle_db_operation(operation):
        """Helper for consistent error handling."""
        try:
            return operation()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {e}")
            return {"success": False, "message": f"Database error: {e}", "count": 0}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error: {e}")
            return {"success": False, "message": f"Unexpected error: {e}", "count": 0}

    @staticmethod
    def save_records(records, batch_size=1000):
        if not records:
            return {"success": False, "message": "No records to save", "count": 0}

        def operation():
            total_saved = 0
            for i in range(0, len(records), batch_size):
                db.session.add_all(records[i:i + batch_size])
                total_saved += len(records[i:i + batch_size])
            db.session.commit()
            return {
                "success": True,
                "message": f"Saved {total_saved} records",
                "count": total_saved,
            }

        return DatabaseService._handle_db_operation(operation)

    @staticmethod
    def bulk_save_records(records, batch_size=1000):
        if not records:
            return {"success": False, "message": "No records to save", "count": 0}

        def model_to_dict(record):
            """Convert SQLAlchemy object to dict (skip primary key)."""
            return {
                col.name: getattr(record, col.name)
                for col in record.__table__.columns
                if col.name != "id" and getattr(record, col.name) is not None
            }

        def operation():
            audit_records = [model_to_dict(r) for r in records if isinstance(r, AuditRecord)]
            ojt_records = [model_to_dict(r) for r in records if isinstance(r, OJTLog)]

            total_saved = 0
            for model_cls, data in [(AuditRecord, audit_records), (OJTLog, ojt_records)]:
                for i in range(0, len(data), batch_size):
                    db.session.bulk_insert_mappings(model_cls, data[i:i + batch_size])
                    total_saved += len(data[i:i + batch_size])

            db.session.commit()
            return {
                "success": True,
                "message": f"Bulk saved {total_saved} records",
                "count": total_saved,
            }

        return DatabaseService._handle_db_operation(operation)

    @staticmethod
    def save_records_by_file(records_per_file, use_bulk=False):
        """Save records grouped by filename."""
        results = {}
        for filename, records in records_per_file.items():
            if isinstance(records, dict) and "error" in records:
                results[filename] = {
                    "success": False,
                    "message": records["error"],
                    "count": 0,
                }
                continue

            if records:
                first = records[0]

                # AuditRecords → use upsert_audit_records
                if isinstance(first, AuditRecord):
                    results[filename] = DatabaseService.upsert_audit_records(records)

                # OJTLogs → use upsert_ojt_logs
                elif isinstance(first, OJTLog):
                    results[filename] = DatabaseService.upsert_ojt_logs(records)

                else:
                    save_func = DatabaseService.bulk_save_records if use_bulk else DatabaseService.save_records
                    results[filename] = save_func(records)
            else:
                results[filename] = {
                    "success": False,
                    "message": "No records to save",
                    "count": 0,
                }

        return results


    
    @staticmethod
    def upsert_audit_records(records):
        """
        Insert or update AuditRecords by matching (aom_no, as_of).
        """
        if not records:
            return {"success": False, "message": "No records to save", "count": 0}

        def operation():
            total_inserted = 0
            total_updated = 0

            for record in records:
                if not isinstance(record, AuditRecord):
                    continue

                # Look for existing record with same aom_no and as_of
                existing = AuditRecord.query.filter_by(
                    aom_no=record.aom_no,
                    as_of=record.as_of
                ).first()

                if existing:
                    # Update fields except id, aom_no, as_of
                    for col in AuditRecord.__table__.columns:
                        col_name = col.name
                        if col_name in ["id", "aom_no", "as_of"]:
                            continue
                        setattr(existing, col_name, getattr(record, col_name))
                    total_updated += 1
                else:
                    db.session.add(record)
                    total_inserted += 1

            db.session.commit()

            return {
                "success": True,
                "message": f"Inserted {total_inserted}, Updated {total_updated} AuditRecords",
                "inserted": total_inserted,
                "updated": total_updated,
                "count": total_inserted + total_updated
            }

        return DatabaseService._handle_db_operation(operation)

    @staticmethod
    def upsert_ojt_logs(records):
        """
        Insert or update OJTLogs by matching (employee_id, date, activity).
        """
        if not records:
            return {"success": False, "message": "No records to save", "count": 0}

        def operation():
            total_inserted = 0
            total_updated = 0

            for record in records:
                if not isinstance(record, OJTLog):
                    continue

                # Cast to string to avoid type mismatches
                employee_id = str(record.employee_id) if record.employee_id is not None else None
                date = str(record.date) if record.date is not None else None
                activity = str(record.activity) if record.activity is not None else None

                existing = OJTLog.query.filter_by(
                    employee_id=employee_id,
                    date=date,
                    activity=activity
                ).first()

                if existing:
                    for col in OJTLog.__table__.columns:
                        col_name = col.name
                        if col_name in ["id", "employee_id", "date", "activity"]:
                            continue
                        setattr(existing, col_name, getattr(record, col_name))
                    total_updated += 1
                else:
                    record.employee_id = employee_id
                    record.date = date
                    record.activity = activity
                    db.session.add(record)
                    total_inserted += 1

            db.session.commit()

            return {
                "success": True,
                "message": f"Inserted {total_inserted}, Updated {total_updated} OJTLogs",
                "inserted": total_inserted,
                "updated": total_updated,
                "count": total_inserted + total_updated
            }

        return DatabaseService._handle_db_operation(operation)
