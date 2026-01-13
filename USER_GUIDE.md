# Horilla HRMS - Complete User Guide

## Table of Contents
1. [Overview](#overview)
2. [Types of Users & Login Systems](#types-of-users--login-systems)
3. [Employee & Admin Login](#employee--admin-login)
4. [Employee Registration & Account Creation](#employee-registration--account-creation)
5. [Candidate Login](#candidate-login)
6. [Dashboards & Features by User Type](#dashboards--features-by-user-type)
7. [Complete Feature List](#complete-feature-list)
8. [Module Descriptions](#module-descriptions)

---

## Overview

Horilla HRMS is a comprehensive Human Resource Management System that manages the entire employee lifecycle from recruitment to offboarding. The system supports multiple user types with different access levels and features.

---

## Types of Users & Login Systems

Horilla HRMS supports **three main types of users**:

1. **Administrators/Superusers** - Full system access
2. **Employees** - Regular employees with role-based permissions
3. **Candidates** - Job applicants with limited self-service access

**Note:** Administrators and Employees use the **same login system** but have different permissions. The system distinguishes between them based on user roles, groups, and permissions rather than separate login portals.

---

## Employee & Admin Login

### Login Process

Both employees and administrators use the same login page at `/login/`

**Steps to Login:**

1. Navigate to the login page (typically `http://localhost:8000/login/`)
2. Enter your **username** (usually your email address)
3. Enter your **password**
4. Click "Secure Sign-in" button

### Login Credentials

- **Username/Email**: Your registered email address
- **Password**: Your account password (set by admin or during first login)

### Default Credentials for New Employees

When employees are created by administrators:
- **Username**: Employee's email address
- **Initial Password**: Employee's phone number (by default)
- **First Login**: Employees should change their password after first login

### Password Recovery

- Click "Forgot password?" link on the login page
- Enter your email address
- Follow the password reset instructions sent to your email

### Authentication Requirements

The system validates:
- Valid username and password
- User account is active
- Associated employee record exists
- Employee record is active (not archived)

---

## Employee Registration & Account Creation

### How Employees Get Accounts

**Important**: Employees **do NOT self-register**. Accounts are created by administrators through:

#### Method 1: Manual Employee Creation (By Admin)
1. Admin navigates to Employee Management
2. Creates new employee record
3. System automatically creates user account with:
   - Username: Employee's email
   - Password: Employee's phone number (temporary)

#### Method 2: Bulk Import (By Admin)
1. Admin uses Excel import feature
2. Uploads spreadsheet with employee data
3. System creates multiple employee accounts automatically
4. Initial password is set to phone number for each employee

#### Method 3: Onboarding Portal (For New Hires)
1. Candidate completes recruitment process
2. Receives onboarding portal link
3. Completes employee creation form via onboarding portal
4. Account is created as part of onboarding process

### First-Time Login for Employees

1. Employee receives credentials from HR/Admin (email + phone number)
2. Logs in using email as username and phone number as password
3. **Should immediately change password** for security
4. Completes profile information if needed

---

## Candidate Login

### Separate Login System for Candidates

Candidates have a **separate login system** that doesn't require employee accounts.

**Login URL**: `/candidate-login/` (or candidate-specific login page)

### Candidate Login Process

1. Navigate to candidate login page
2. Enter **Email** address (used during application)
3. Enter **Mobile/Phone Number** (used during application)
4. Click login

**Note**: Candidates use email and mobile number as credentials (not username/password)

### Candidate Features

Candidates can:
- View their application status
- Track recruitment pipeline progress
- Update profile information
- Upload documents
- Check interview schedules (if applicable)

### Candidate Registration

Candidates register during the job application process:
1. Apply for a job position
2. Fill out application form
3. Provide email and mobile number
4. Submit application
5. Use same email and mobile to login and track status

---

## Dashboards & Features by User Type

### Administrator Dashboard

**Location**: Main dashboard (`/`)

**Features Available:**
- **Full System Access** to all modules
- **Employee Management**: Create, edit, delete, archive employees
- **User Management**: Assign permissions, create user groups
- **Company Settings**: Manage companies, departments, job positions
- **System Configuration**: Attendance settings, leave types, payroll setup
- **Reports & Analytics**: All reports across all modules
- **Recruitment Management**: Full recruitment pipeline control
- **Onboarding & Offboarding**: Complete process management
- **Payroll Management**: Process payroll, manage allowances/deductions
- **Asset Management**: Allocate and track assets
- **Helpdesk Administration**: Manage tickets, categories, FAQs
- **Performance Management**: Set objectives, review periods
- **Attendance Management**: Validate attendance, manage shifts

**Key Administrative Tasks:**
- Initialize database (first-time setup)
- Load demo data (optional)
- Configure system settings
- Assign permissions to employees
- Manage user groups
- Configure workflows and approvals

### Employee Dashboard

**Location**: Main dashboard (`/`)

**Features Available (Based on Permissions):**

#### Common Employee Features:
- **Personal Profile**: View and edit own profile
- **My Attendance**: View own attendance records, request attendance corrections
- **My Leave**: Apply for leave, view leave balance, track leave requests
- **My Assets**: View allocated assets, request assets
- **My Payroll**: View payslips, loan accounts, reimbursement requests
- **My Objectives**: View assigned objectives and key results (PMS)
- **My Feedback**: Give and receive feedback
- **My Documents**: View and upload documents
- **My Tickets**: Create and track helpdesk tickets
- **Notifications**: System notifications and alerts

#### Manager-Level Features (If Employee is a Manager):
- **Team Management**: View team members
- **Leave Approvals**: Approve/reject leave requests from team
- **Attendance Validation**: Validate team attendance
- **Shift Requests**: Approve shift change requests
- **Work Type Requests**: Approve work type requests
- **Overtime Approvals**: Approve overtime requests
- **Team Objectives**: View and manage team objectives
- **Team Feedback**: View team performance feedback

#### Permission-Based Features:
Employees may have access to additional features based on assigned permissions:
- Recruitment (if assigned recruitment permissions)
- Onboarding management
- Asset allocation (if manager/HR)
- Payroll processing (if HR/Finance)
- Report viewing (various reports based on permissions)

**Employee Dashboard Widgets:**
- Birthday reminders
- Upcoming holidays
- Pending approvals (for managers)
- Leave balance
- Attendance summary
- Recent notifications
- Customizable charts (based on permissions)

### Candidate Dashboard

**Location**: Candidate self-tracking page

**Features Available:**
- **Application Status**: View current stage in recruitment pipeline
- **Profile Information**: Update personal details, contact information
- **Documents**: Upload/view required documents
- **Interview Schedule**: View scheduled interviews (if applicable)
- **Application History**: View all applications
- **Status Updates**: Real-time updates on application progress

---

## Complete Feature List

Horilla HRMS includes the following modules and features:

### 1. Recruitment Management
- Job posting and job position management
- Candidate application and tracking
- Recruitment pipeline (stages)
- Interview scheduling
- Candidate evaluation and rating
- Offer letter generation
- Recruitment analytics and reports
- Candidate self-tracking portal
- Recruitment surveys and questionnaires
- Email templates for recruitment

### 2. Employee Management
- Employee profile management
- Employee directory
- Organization chart
- Employee tagging and categorization
- Employee import/export (Excel)
- Employee documents
- Employee notes and history
- Birthday reminders
- Employee dashboard and analytics
- Employee archiving/activation

### 3. Onboarding
- Onboarding pipeline
- Onboarding checklist
- Employee creation from onboarding
- Document collection
- Task assignment
- Welcome portal for new hires
- Onboarding analytics

### 4. Attendance Management
- Clock in/clock out
- Attendance records and history
- Shift management
- Rotating shifts
- Work type management (office, remote, hybrid)
- Overtime tracking
- Attendance validation
- Late come/Early out tracking
- Attendance requests (corrections)
- Attendance reports and analytics
- Biometric device integration
- Face detection for attendance
- Geo-fencing for attendance
- Attendance dashboard

### 5. Leave Management
- Leave types configuration
- Leave allocation
- Leave requests and approvals
- Leave balance tracking
- Holiday calendar
- Company leave calendar
- Leave reports and analytics
- Leave dashboard
- Leave allocation requests
- Compensatory leave
- Leave carry forward

### 6. Payroll Management
- Employee payslip generation
- Salary structure management
- Allowances and deductions
- Tax management (filing status)
- Loan account management
- Reimbursement management
- Contract management
- Payroll dashboard
- Payroll reports
- Multi-currency support

### 7. Performance Management System (PMS)
- Objective and Key Results (OKR) framework
- Performance periods
- Employee objectives
- Key results tracking
- Performance feedback
- Feedback templates
- Performance reviews
- Performance dashboard
- Objective status tracking
- Performance analytics

### 8. Asset Management
- Asset categories
- Asset allocation to employees
- Asset request and approval
- Asset tracking
- Asset reports
- Asset history

### 9. Offboarding
- Offboarding pipeline
- Exit interview
- Clearance checklist
- Asset return tracking
- Document handover
- Offboarding analytics

### 10. Helpdesk
- Ticket creation and management
- Ticket categories and types
- FAQ management
- Ticket assignment
- Ticket status tracking
- Ticket history
- Helpdesk reports

### 11. Project Management (If Enabled)
- Project creation and management
- Task assignment
- Project dashboard
- Project tracking
- Project reports

### 12. Base/System Features
- Company management (multi-company support)
- Department management
- Job position management
- Job role management
- User group management
- Permission management
- Employee type management
- Work type management
- Currency management
- Date and time settings
- Mail server configuration
- Email templates
- Announcements
- Notifications
- Backup and restore
- LDAP integration (optional)
- White-labeling
- Multi-language support

---

## Module Descriptions

### Recruitment Module
Manage the entire recruitment lifecycle from job posting to candidate onboarding. Features include job position management, candidate tracking, interview scheduling, evaluation, and analytics.

### Employee Module
Comprehensive employee database management. Store employee information, manage profiles, view organization structure, and track employee lifecycle.

### Onboarding Module
Streamline new employee onboarding process with checklists, document collection, task assignments, and automated workflows.

### Attendance Module
Track employee attendance through various methods (manual, biometric, face detection, geo-fencing). Manage shifts, work types, overtime, and generate attendance reports.

### Leave Module
Manage employee leave requests, track leave balances, configure leave types, manage holiday calendars, and generate leave reports.

### Payroll Module
Process employee payroll, manage salary structures, handle allowances/deductions, process loans and reimbursements, generate payslips, and manage tax-related information.

### Performance Management System (PMS)
Set and track employee objectives and key results (OKRs), collect performance feedback, conduct performance reviews, and generate performance reports.

### Asset Module
Track company assets, allocate assets to employees, manage asset requests, and maintain asset history and reports.

### Offboarding Module
Manage employee exit process with clearances, exit interviews, asset returns, and document handovers.

### Helpdesk Module
Internal support ticket system for employees to raise issues, request assistance, and track resolution status.

### Project Module (Optional)
Manage projects, assign tasks, track progress, and generate project reports (if enabled).

---

## User Roles & Permissions

### Permission System
Horilla uses Django's permission system with custom permissions for granular access control.

**Permission Levels:**
- **View**: Read-only access
- **Add**: Create new records
- **Change**: Edit existing records
- **Delete**: Remove records
- **Custom Permissions**: Module-specific permissions

### Common Permission Groups
- **Employee Permissions**: Basic employee access
- **Manager Permissions**: Team management and approvals
- **HR Permissions**: Employee and recruitment management
- **Finance Permissions**: Payroll and financial data
- **Admin Permissions**: Full system access

### Permission Assignment
- Permissions can be assigned individually to users
- User groups can be created with specific permissions
- Employees can be assigned to groups
- Permissions are checked on every action

---

## Getting Started

### For Administrators (First-Time Setup)
1. Run database initialization (from login page)
2. Create super admin account
3. Set up company, department, job positions
4. Configure system settings
5. Create employee accounts
6. Assign permissions and user groups

### For Employees (First Login)
1. Receive login credentials from HR/Admin
2. Login with email and initial password (phone number)
3. Change password immediately
4. Complete profile information
5. Explore available features based on permissions

### For Candidates
1. Apply for job positions
2. Receive application confirmation
3. Use email and mobile to login to candidate portal
4. Track application status
5. Complete required documents/tasks

---

## Support & Documentation

For additional support:
- Check the main README.md for installation and setup
- Visit official Horilla documentation
- Contact system administrator
- Review module-specific help sections within the application

---

## Security Notes

- Always change default passwords
- Use strong, unique passwords
- Enable two-factor authentication if available
- Regularly review user permissions
- Keep system updated
- Follow organizational security policies

---

*This guide covers the main features and workflows of Horilla HRMS. Specific features may vary based on your system configuration and permissions.*


