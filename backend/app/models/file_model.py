from .. import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import validates
import re


class AuditRecord(db.Model):
    """SQLAlchemy model for AuditRecord with built-in validation"""
    __tablename__ = 'audit_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Required fields
    calendar_year = db.Column(db.Integer, nullable=False)
    as_of = db.Column(db.String(255), nullable=False)
    aom_no = db.Column(db.String(255), nullable=False)
    
    # Optional fields
    audit_type = db.Column(db.String(255), nullable=True)
    audit_observation = db.Column(db.String(255), nullable=True)
    audit_observation_description = db.Column(db.Text, nullable=True)
    audit_recommendations = db.Column(db.Text, nullable=True)
    agency_action_plan = db.Column(db.Text, nullable=True)
    person_or_department_responsible = db.Column(db.String(255), nullable=True)
    target_implementation_from = db.Column(db.String(255), nullable=True)
    target_implementation_to = db.Column(db.String(255), nullable=True)
    management_comment = db.Column(db.Text, nullable=True)
    auditors_rejoinder = db.Column(db.Text, nullable=True)
    actions_to_be_taken = db.Column(db.Text, nullable=True)
    consolidated_by = db.Column(db.String(255), nullable=True)
    noted_by = db.Column(db.String(255), nullable=True)

class OJTLog(db.Model):
    """SQLAlchemy model for OJT Log with built-in validation"""
    __tablename__ = 'ojt_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Required fields
    employee_id = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    employee_name = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    activity = db.Column(db.Text, nullable=False)
    
    # Optional fields
    image = db.Column(db.String(500), nullable=True)
    address = db.Column(db.Text, nullable=True)
