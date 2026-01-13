# MyHRMS  - Comprehensive Feature Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core Modules](#core-modules)
3. [Employee Management](#employee-management)
4. [Recruitment Management](#recruitment-management)
5. [Onboarding](#onboarding)
6. [Attendance Management](#attendance-management)
7. [Leave Management](#leave-management)
8. [Payroll Management](#payroll-management)
9. [Performance Management System (PMS)](#performance-management-system-pms)
10. [Asset Management](#asset-management)
11. [Offboarding](#offboarding)
12. [Helpdesk](#helpdesk)
13. [Project Management](#project-management)
14. [Biometric Integration](#biometric-integration)
15. [Additional Features](#additional-features)

---

## Overview

**MyHRMS ** is a comprehensive, open-source Human Resource Management System built on Django framework. It provides end-to-end HR management capabilities from recruitment to offboarding, with advanced features for attendance tracking, payroll processing, performance management, and more.

**Technology Stack:**
- **Backend:** Django 4.1.4+
- **Database:** PostgreSQL (recommended)
- **Frontend:** Bootstrap, HTML5, CSS3, JavaScript
- **Architecture:** Multi-tenant, Company-based isolation
- **License:** LGPL

---

## Core Modules

### Base Module
**Purpose:** Foundation module providing core organizational structure and shared functionality.

**Key Features:**
- **Multi-Company Management:** Support for multiple companies with data isolation
- **Organizational Hierarchy:** Department, Job Position, Job Role management
- **Work Type Management:** Standard, Rotating, and Custom work types
- **Shift Management:** Flexible shift scheduling with rotating shifts
- **Company Leaves & Holidays:** Configurable company-wide leaves and holiday calendars
- **Email Configuration:** Dynamic email templates and SMTP configuration
- **Announcements:** Company-wide announcement system with expiration dates
- **Dynamic Fields:** Custom field support for extensibility
- **IP-based Access Control:** Restrict attendance check-in by IP address

**MVP (Most Valuable Point):** Multi-tenant architecture with complete data isolation enables organizations to manage multiple subsidiaries or clients within a single instance while maintaining strict data separation.

---

## Employee Management

**Purpose:** Centralized employee lifecycle management from onboarding to offboarding.

### Core Features

#### 1. Employee Profile Management
- **Comprehensive Employee Records:** Personal information, contact details, emergency contacts
- **Profile Images:** Avatar management with SVG/image validation
- **Badge ID System:** Unique employee identification with prefix configuration
- **Employee Tags:** Categorization and tagging system for employees
- **Work Information:** Department, job position, reporting manager, shift assignment
- **Bank Details:** Secure bank account information storage
- **Employee Notes:** Internal notes with file attachments
- **Archive Management:** Employee archiving with dependency checking

**MVP:** Complete employee lifecycle tracking with audit trails ensures compliance and provides comprehensive employee history.

#### 2. Employee Work Information
- **Department Assignment:** Link employees to departments
- **Job Position & Role:** Hierarchical job structure
- **Reporting Manager:** Manager-subordinate relationships
- **Shift Assignment:** Work shift allocation
- **Work Type:** Standard, remote, hybrid, rotating work types
- **Company Assignment:** Multi-company employee assignment
- **Joining Date & Contract End Date:** Employment period tracking
- **Basic Salary & Hourly Rate:** Compensation information
- **Experience Calculation:** Automatic experience calculation based on joining date
- **Location Tracking:** Work location assignment

**MVP:** Centralized work information management enables accurate organizational reporting and compliance with labor regulations.

#### 3. Employee Policies
- **Policy Management:** Create and manage company policies
- **Visibility Control:** Company-wide or department-specific policies
- **Policy Attachments:** Document attachments for policies
- **Multi-Company Support:** Policies scoped to specific companies

**MVP:** Policy distribution system ensures all employees have access to updated company policies, reducing compliance risks.

#### 4. Disciplinary Actions
- **Action Types:** Warning, Suspension, Dismissal
- **Login Blocking:** Automatic login restriction based on action type
- **Duration Management:** Time-based disciplinary periods (days/hours)
- **Attachment Support:** Document evidence for disciplinary actions
- **Multi-Employee Actions:** Apply actions to multiple employees

**MVP:** Automated disciplinary workflow with login blocking ensures policy enforcement and reduces manual intervention.

#### 5. Bonus Points System
- **Point Allocation:** Award bonus points to employees
- **Encashment Conditions:** Configurable point redemption rules
- **Point Tracking:** Complete history of point allocation and redemption
- **Integration:** Integrated with PMS and Project modules for automatic point allocation

**MVP:** Gamification system incentivizes performance and provides flexible reward mechanisms beyond monetary compensation.

---

## Recruitment Management

**Purpose:** End-to-end recruitment process from job posting to candidate hiring.

### Core Features

#### 1. Recruitment Process
- **Job Posting:** Create recruitment campaigns for job positions
- **Event-Based Recruitment:** Multi-position recruitment events
- **Vacancy Management:** Track available positions
- **Recruitment Managers:** Assign managers to recruitment processes
- **Stage Management:** Customizable recruitment stages (Initial, Applied, Test, Interview, Hired, Cancelled)
- **Stage Managers:** Assign managers to specific stages
- **Sequence Management:** Order stages in recruitment pipeline
- **Publishing Control:** Publish to public recruitment page
- **LinkedIn Integration:** Post jobs directly to LinkedIn
- **Skills Management:** Tag required skills for positions

**MVP:** Visual pipeline view with stage-based workflow provides transparency and accelerates hiring decisions.

#### 2. Candidate Management
- **Candidate Profiles:** Comprehensive candidate information
- **Resume Management:** PDF resume upload and storage
- **Profile Images:** Candidate photo management
- **Source Tracking:** Application source (Form, Software, Other)
- **Referral System:** Employee referral tracking
- **Stage Progression:** Move candidates through recruitment stages
- **Interview Scheduling:** Schedule and track interviews
- **Offer Letter Management:** Track offer letter status (Not Sent, Sent, Accepted, Rejected, Joined)
- **Candidate Rating:** Rate candidates with 5-star system
- **Conversion to Employee:** Convert hired candidates to employees

**MVP:** Complete candidate lifecycle tracking with interview scheduling and offer management streamlines the hiring process.

#### 3. Survey & Assessment
- **Survey Templates:** Create reusable survey templates
- **Question Types:** Multiple choice, text, number, percentage, date, file upload, rating
- **Mandatory Questions:** Mark questions as required
- **Question Ordering:** Customize question sequence
- **Survey Answers:** Store candidate responses in JSON format
- **Attachment Support:** File uploads in surveys

**MVP:** Customizable survey system enables standardized candidate assessment and data collection.

#### 4. Skill Zone (Talent Pool)
- **Talent Pool Management:** Maintain database of potential candidates
- **Skill-Based Categorization:** Organize candidates by skills
- **Future Recruitment:** Quick access to qualified candidates
- **Reason Tracking:** Track why candidates are in talent pool

**MVP:** Talent pool feature reduces time-to-hire by maintaining a database of pre-qualified candidates.

#### 5. Rejection Management
- **Reject Reasons:** Predefined rejection reason templates
- **Rejection Tracking:** Track why candidates were rejected
- **Multiple Reasons:** Assign multiple reasons per rejection

**MVP:** Rejection reason tracking provides insights for improving recruitment processes and candidate experience.

#### 6. Document Request System
- **Document Requests:** Request additional documents from candidates
- **Format Validation:** Specify required file formats (PDF, DOCX, XLSX, JPG, PNG, etc.)
- **Size Limits:** Set maximum file size restrictions
- **Status Tracking:** Track document request status (Requested, Approved, Rejected)
- **Rejection Reasons:** Document rejection with reasons

**MVP:** Automated document collection reduces manual follow-up and ensures compliance with hiring requirements.

---

## Onboarding

**Purpose:** Streamlined onboarding process for new hires.

### Core Features

#### 1. Onboarding Stages
- **Stage Management:** Create custom onboarding stages
- **Stage Managers:** Assign managers to onboarding stages
- **Sequence Control:** Order stages in onboarding process
- **Final Stage Marking:** Mark stages as final completion stages
- **Recruitment Integration:** Link onboarding to recruitment processes

**MVP:** Stage-based onboarding ensures consistent new hire experience and reduces onboarding time.

#### 2. Onboarding Tasks
- **Task Creation:** Define tasks for each onboarding stage
- **Task Managers:** Assign responsible managers for tasks
- **Candidate Assignment:** Assign tasks to specific candidates
- **Task Status:** Track task completion (Todo, Scheduled, Ongoing, Stuck, Done)
- **Task Completion Ratio:** Monitor completion progress

**MVP:** Task-based onboarding checklist ensures no critical steps are missed during employee onboarding.

#### 3. Candidate Stage Tracking
- **Stage Progression:** Track candidate progress through stages
- **End Date Tracking:** Automatic end date when final stage is reached
- **Completion Metrics:** Task completion ratio per stage

**MVP:** Real-time progress tracking enables managers to identify bottlenecks and ensure timely onboarding completion.

#### 4. Onboarding Portal
- **Portal Access:** Token-based portal access for candidates
- **Profile Management:** Candidates can update their profiles
- **Usage Tracking:** Track portal access and usage

**MVP:** Self-service portal reduces administrative burden and improves candidate experience during onboarding.

---

## Attendance Management

**Purpose:** Comprehensive attendance tracking with multiple validation and approval mechanisms.

### Core Features

#### 1. Attendance Recording
- **Check-In/Check-Out:** Manual and biometric attendance recording
- **Multiple Activities:** Track multiple check-in/check-out activities per day
- **Date Flexibility:** Support for cross-day shifts (night shifts)
- **Minimum Hour Tracking:** Track worked hours vs. required minimum hours
- **Overtime Calculation:** Automatic overtime calculation
- **Overtime Approval:** Manager approval workflow for overtime
- **Attendance Validation:** Validation workflow for attendance records
- **Batch Attendance:** Group attendance operations

**MVP:** Multi-activity tracking with automatic overtime calculation provides accurate time tracking for complex work schedules.

#### 2. Shift Management Integration
- **Shift Assignment:** Link attendance to employee shifts
- **Shift Day Tracking:** Track attendance by shift day
- **Night Shift Detection:** Automatic night shift identification
- **Work Type Integration:** Link attendance to work types

**MVP:** Shift-aware attendance system ensures accurate tracking for employees with varying schedules.

#### 3. Attendance Requests
- **Create Request:** Employees can request attendance record creation
- **Update Request:** Request updates to existing attendance records
- **Re-validation Request:** Request re-validation of attendance
- **Request Comments:** Comment thread on attendance requests
- **File Attachments:** Attach supporting documents
- **Approval Workflow:** Manager approval for attendance requests

**MVP:** Self-service attendance correction reduces HR workload while maintaining control through approval workflows.

#### 4. Attendance Validation Conditions
- **Auto-Approval:** Automatic validation for worked hours below threshold
- **Overtime Auto-Approve:** Automatic overtime approval based on conditions
- **Overtime Cutoff:** Maximum overtime limit configuration
- **Minimum Overtime:** Minimum overtime threshold for auto-approval

**MVP:** Automated validation rules reduce manual review workload while ensuring policy compliance.

#### 5. Grace Time Management
- **Grace Time Configuration:** Set grace time for check-in/check-out
- **Clock-In Grace:** Separate grace time for check-in
- **Clock-Out Grace:** Separate grace time for check-out
- **Default Grace Time:** Company-wide default grace time

**MVP:** Grace time feature provides flexibility for employees while maintaining attendance accuracy.

#### 6. Hour Account (Monthly Summary)
- **Worked Hours:** Monthly worked hours calculation
- **Pending Hours:** Hours pending to meet minimum requirement
- **Overtime Hours:** Total overtime hours per month
- **Validated Hours:** Hours that have been validated
- **Not Validated Hours:** Hours pending validation
- **Not Approved OT:** Overtime hours pending approval

**MVP:** Monthly hour account provides comprehensive view of employee attendance for payroll and compliance purposes.

#### 7. Late Come & Early Out Tracking
- **Automatic Detection:** System detects late arrivals and early departures
- **Penalty Integration:** Link to penalty system
- **Tracking History:** Complete history of late/early instances

**MVP:** Automatic detection of attendance violations ensures consistent policy enforcement.

#### 8. Work Records
- **Unified View:** Single view of attendance and leave records
- **Record Types:** Present, Half Day Present, Absent, Holiday, Conflict, Draft
- **Day Percentage:** Calculate work percentage per day
- **Conflict Resolution:** Identify conflicts between attendance and leave

**MVP:** Unified work record view eliminates discrepancies between attendance and leave systems.

---

## Leave Management

**Purpose:** Comprehensive leave management with flexible policies and approval workflows.

### Core Features

#### 1. Leave Type Configuration
- **Leave Types:** Create custom leave types (Sick, Casual, Annual, etc.)
- **Paid/Unpaid:** Configure leave as paid or unpaid
- **Leave Limits:** Set maximum leave days per period
- **Reset Periods:** Yearly, Monthly, Weekly reset options
- **Reset Configuration:** Custom reset dates (specific day of month/week)
- **Carry Forward:** Enable leave carry forward to next period
- **Carry Forward Limits:** Maximum carry forward days
- **Carry Forward Expiry:** Expiry period for carried forward leaves
- **Approval Requirement:** Require approval or auto-approve
- **Attachment Requirement:** Mandatory document upload
- **Holiday Exclusion:** Exclude holidays from leave calculation
- **Company Leave Exclusion:** Exclude company leaves from calculation
- **Encashment:** Enable leave encashment
- **Compensatory Leave:** Support for compensatory leave types

**MVP:** Flexible leave type configuration supports diverse organizational policies while maintaining compliance.

#### 2. Leave Allocation
- **Automatic Allocation:** Automatic leave allocation based on reset periods
- **Manual Allocation:** Manual leave allocation requests
- **Allocation Requests:** Employee-initiated allocation requests
- **Approval Workflow:** Manager approval for allocation requests
- **Available Days:** Track available leave days
- **Carry Forward Days:** Track carried forward days
- **Total Leave Days:** Sum of available and carry forward days

**MVP:** Automated allocation with manual override capability ensures accurate leave balance tracking.

#### 3. Leave Requests
- **Request Creation:** Employees create leave requests
- **Date Range Selection:** Start and end date selection
- **Breakdown Options:** Full day, First half, Second half
- **Requested Days Calculation:** Automatic calculation of leave days
- **Effective Days:** Days after excluding holidays/company leaves
- **Overlapping Detection:** Prevent overlapping leave requests
- **Leave Clash Detection:** Identify conflicts with other employees
- **Attachment Support:** Upload supporting documents
- **Status Tracking:** Requested, Approved, Rejected, Cancelled
- **Rejection Reasons:** Document rejection reasons

**MVP:** Intelligent leave request system with conflict detection prevents scheduling issues and ensures adequate coverage.

#### 4. Multiple Approval Workflow
- **Condition-Based Approval:** Different approval chains based on leave duration
- **Multiple Managers:** Sequential approval from multiple managers
- **Approval Sequence:** Define approval order
- **Department-Based:** Approval based on department
- **Condition Operators:** Equal, Not Equal, Less Than, Greater Than, Range
- **Approval Status:** Track approval status per manager

**MVP:** Flexible approval workflow adapts to organizational hierarchy and ensures proper authorization.

#### 5. Leave Restrictions
- **Date Restrictions:** Restrict leave requests for specific date ranges
- **Department-Based:** Apply restrictions to specific departments
- **Job Position-Based:** Apply restrictions to specific positions
- **Leave Type Filtering:** Include/exclude specific leave types
- **Reason Tracking:** Document restriction reasons

**MVP:** Leave restriction system prevents leave requests during critical business periods.

#### 6. Compensatory Leave
- **Attendance Integration:** Convert attendance to compensatory leave
- **Automatic Allocation:** Automatic allocation upon approval
- **Leave Type:** Dedicated compensatory leave type

**MVP:** Compensatory leave feature rewards employees for working on holidays or overtime.

#### 7. Holiday Management
- **Holiday Calendar:** Create company holiday calendar
- **Recurring Holidays:** Set up recurring annual holidays
- **Date Range:** Support for multi-day holidays
- **Company-Specific:** Holidays scoped to companies

**MVP:** Centralized holiday management ensures consistent holiday calendar across the organization.

#### 8. Company Leave Configuration
- **Week-Based Leaves:** Configure leaves based on week of month
- **Day-Based Leaves:** Configure leaves based on day of week
- **Automatic Calculation:** System calculates company leave dates

**MVP:** Flexible company leave configuration supports various leave policies (e.g., second Saturday off).

---

## Payroll Management

**Purpose:** Comprehensive payroll processing with flexible calculation rules.

### Core Features

#### 1. Contract Management
- **Contract Creation:** Create employment contracts
- **Contract Types:** Salary, Hourly, Commission-based
- **Pay Frequency:** Weekly, Monthly, Semi-Monthly
- **Wage Types:** Daily, Monthly, Hourly
- **Contract Status:** Draft, Active, Expired, Terminated
- **Notice Period:** Configurable notice period
- **Contract Documents:** Attach contract documents
- **Leave Deduction:** Configure leave deduction from basic pay
- **Daily Leave Amount:** Calculate daily leave deduction amount

**MVP:** Contract-based payroll ensures accurate compensation calculation based on employment terms.

#### 2. Filing Status (Tax Configuration)
- **Tax Filing Status:** Configure tax filing status
- **Calculation Basis:** Basic Pay, Gross Pay, Taxable Gross Pay
- **Python Code Support:** Custom calculation logic using Python
- **Company-Specific:** Tax rules per company

**MVP:** Flexible tax configuration supports various tax regimes and calculation methods.

#### 3. Allowances
- **Allowance Types:** Fixed amount or percentage-based
- **Calculation Basis:** Basic Pay, Children, Overtime, Shift, Work Type, Attendance
- **Condition-Based:** Apply allowances based on employee conditions
- **Employee Targeting:** All employees, specific employees, or exclude employees
- **One-Time Allowances:** Date-specific allowances
- **Taxable/Non-Taxable:** Configure tax treatment
- **Maximum Limits:** Set maximum allowance limits
- **If Conditions:** Apply allowances based on pay head conditions
- **Range Conditions:** Apply allowances within salary ranges

**MVP:** Flexible allowance system supports complex compensation structures while maintaining calculation accuracy.

#### 4. Deductions
- **Deduction Types:** Fixed amount or percentage-based
- **Calculation Basis:** Basic Pay, Gross Pay, Taxable Gross Pay, Net Pay
- **Tax Deductions:** Mark deductions as tax
- **Pre-Tax Deductions:** Deductions before tax calculation
- **Condition-Based:** Apply deductions based on employee conditions
- **Employee Targeting:** All employees, specific employees, or exclude employees
- **One-Time Deductions:** Date-specific deductions
- **Maximum Limits:** Set maximum deduction limits
- **Update Compensation:** Update pay heads before other calculations
- **Employer Rate:** Separate employer contribution rates

**MVP:** Comprehensive deduction system handles taxes, benefits, and other deductions accurately.

#### 5. Payslip Generation
- **Manual Generation:** Create payslips manually
- **Auto-Generation:** Automatic payslip generation on specified day
- **Pay Period:** Start and end date for pay period
- **Pay Head Data:** JSON storage of all pay head calculations
- **Status Tracking:** Draft, Review Ongoing, Confirmed, Paid
- **Employee Notification:** Send payslips to employees
- **Batch Processing:** Group payslips for batch operations
- **Reference Numbers:** Unique reference for each payslip

**MVP:** Automated payslip generation reduces manual effort and ensures timely payroll processing.

#### 6. Loan Management
- **Loan Types:** Loan, Advanced Salary, Penalty/Fine
- **Loan Amount:** Principal loan amount
- **Installment Configuration:** Number of installments and amount
- **Installment Schedule:** Automatic schedule generation
- **Installment Start Date:** When deductions begin
- **Settlement Tracking:** Track loan settlement
- **Settlement Date:** Automatic settlement date tracking
- **Asset Integration:** Link loans to asset purchases

**MVP:** Integrated loan management simplifies employee loan processing and tracking.

#### 7. Reimbursement
- **Reimbursement Types:** General reimbursement, Bonus encashment, Leave encashment
- **Request Management:** Employee-initiated reimbursement requests
- **Attachment Support:** Upload supporting documents
- **Approval Workflow:** Manager approval process
- **Status Tracking:** Requested, Approved, Rejected
- **Allowance Integration:** Automatic allowance creation upon approval
- **Leave Encashment:** Convert leave days to monetary reimbursement
- **Bonus Encashment:** Convert bonus points to monetary reimbursement

**MVP:** Self-service reimbursement reduces administrative overhead while maintaining control through approval workflows.

#### 8. Encashment Settings
- **Leave Amount:** Configure monetary value per leave day
- **Bonus Amount:** Configure monetary value per bonus point

**MVP:** Configurable encashment rates provide flexibility in reward and leave policies.

---

## Performance Management System (PMS)

**Purpose:** Comprehensive performance management with OKR framework and 360-degree feedback.

### Core Features

#### 1. Objectives & Key Results (OKR)
- **Objective Creation:** Create organizational and employee objectives
- **Key Results:** Define measurable key results for objectives
- **Progress Types:** Percentage, Number, Currency (USD, INR, EUR)
- **Target Values:** Set target values for key results
- **Duration Management:** Set objective duration (days, months, years)
- **Start/End Dates:** Define objective timeline
- **Status Tracking:** On Track, Behind, Closed, At Risk, Not Started
- **Progress Percentage:** Automatic progress calculation
- **Manager Assignment:** Assign managers to objectives
- **Assignee Management:** Assign employees to objectives
- **Self-Progress Update:** Allow employees to update their own progress

**MVP:** OKR framework provides structured goal-setting and tracking, aligning individual performance with organizational objectives.

#### 2. Employee Objectives
- **Objective Assignment:** Assign objectives to employees
- **Custom Objectives:** Create employee-specific objectives
- **Key Result Assignment:** Assign key results to objectives
- **Progress Tracking:** Track objective and key result progress
- **Status Updates:** Update objective status
- **Comments:** Add comments to objectives
- **Archive Management:** Archive completed objectives

**MVP:** Employee-specific objective tracking enables personalized performance management.

#### 3. Key Results Management
- **Key Result Creation:** Create reusable key result templates
- **Progress Calculation:** Automatic progress based on current vs. target value
- **Start/Current/Target Values:** Track key result values
- **Duration Configuration:** Set key result duration
- **Status Tracking:** Track key result status

**MVP:** Measurable key results provide clear performance indicators and enable data-driven performance evaluation.

#### 4. 360-Degree Feedback
- **Feedback Creation:** Create feedback cycles
- **Review Cycles:** Define feedback review periods
- **Manager Feedback:** Collect feedback from managers
- **Colleague Feedback:** Collect feedback from colleagues
- **Subordinate Feedback:** Collect feedback from subordinates
- **Other Employees:** Include other employees in feedback
- **Question Templates:** Use predefined question templates
- **Custom Questions:** Create custom feedback questions
- **Question Types:** Text, Rating, Boolean, Multi-choice, Likert scale
- **Key Result Integration:** Link feedback to key results
- **Cyclic Feedback:** Set up recurring feedback cycles
- **Status Tracking:** Track feedback completion status

**MVP:** 360-degree feedback provides comprehensive performance insights from multiple perspectives.

#### 5. Anonymous Feedback
- **Anonymous Submission:** Submit feedback anonymously
- **Feedback Types:** General, Employee-specific, Department-specific, Job Position-specific
- **Subject & Description:** Detailed feedback content
- **Unique ID:** System-generated anonymous feedback ID

**MVP:** Anonymous feedback encourages honest feedback and improves organizational culture.

#### 6. Question Templates
- **Template Creation:** Create reusable question templates
- **Question Management:** Add questions to templates
- **Question Types:** Text, Rating, Boolean, Multi-choice, Likert
- **Question Options:** Configure options for multi-choice questions
- **Company-Specific:** Templates scoped to companies

**MVP:** Reusable question templates standardize feedback collection and reduce setup time.

#### 7. Meetings
- **Meeting Creation:** Schedule performance review meetings
- **Participant Management:** Add employees and managers
- **Question Template Integration:** Use templates for meeting discussions
- **Response Collection:** Collect meeting responses
- **Response Visibility:** Control response visibility
- **Date & Time:** Schedule meeting date and time

**MVP:** Integrated meeting system streamlines performance review discussions and documentation.

#### 8. Bonus Point Integration
- **Automatic Allocation:** Award bonus points for objective/key result completion
- **Condition-Based:** Points based on completion conditions
- **Model Integration:** Link to Objectives, Key Results, Tasks, Projects
- **Applicable For:** Owner, Members, Managers
- **Completion Tracking:** Track completion dates vs. end dates

**MVP:** Performance-based bonus points incentivize goal achievement and create gamified performance culture.

---

## Asset Management

**Purpose:** Complete asset lifecycle management from procurement to disposal.

### Core Features

#### 1. Asset Categories
- **Category Management:** Organize assets by categories
- **Category Description:** Detailed category information
- **Multi-Company Support:** Categories scoped to companies

**MVP:** Category-based organization simplifies asset management and reporting.

#### 2. Asset Lots/Batches
- **Batch Management:** Group assets by purchase batches
- **Batch Number:** Unique batch identification
- **Batch Description:** Detailed batch information

**MVP:** Batch tracking enables efficient asset procurement and inventory management.

#### 3. Asset Management
- **Asset Creation:** Register assets in the system
- **Asset Tracking ID:** Unique asset identification
- **Asset Details:** Name, description, purchase date, purchase cost
- **Category Assignment:** Link assets to categories
- **Batch Assignment:** Link assets to batches
- **Status Tracking:** In Use, Available, Not-Available
- **Current User:** Track asset assignment
- **Expiry Date:** Track asset expiration
- **Expiry Notifications:** Notify before asset expiry

**MVP:** Complete asset lifecycle tracking ensures optimal asset utilization and compliance.

#### 4. Asset Assignment
- **Assignment Management:** Assign assets to employees
- **Assignment Date:** Track assignment date
- **Assigned By:** Track who assigned the asset
- **Return Management:** Track asset returns
- **Return Date:** Record return date
- **Return Condition:** Document asset condition on return
- **Return Status:** Healthy, Minor damage, Major damage
- **Return Images:** Upload images of asset condition
- **Assign Images:** Document asset condition at assignment
- **Return Requests:** Employee-initiated return requests

**MVP:** Complete assignment tracking with condition documentation protects organizational assets and ensures accountability.

#### 5. Asset Requests
- **Request Management:** Employees request assets
- **Category Selection:** Request by asset category
- **Request Description:** Detailed request information
- **Status Tracking:** Requested, Approved, Rejected
- **Approval Workflow:** Manager approval process

**MVP:** Self-service asset requests streamline asset allocation while maintaining approval control.

#### 6. Asset Reports
- **Report Creation:** Create asset reports
- **Report Title:** Descriptive report titles
- **Document Attachments:** Attach documents to reports

**MVP:** Asset reporting enables maintenance tracking and asset history documentation.

---

## Offboarding

**Purpose:** Structured employee exit process ensuring smooth transitions.

### Core Features

#### 1. Offboarding Process
- **Process Creation:** Create offboarding processes
- **Process Title & Description:** Define offboarding process
- **Manager Assignment:** Assign offboarding managers
- **Status Tracking:** Ongoing, Completed
- **Company-Specific:** Processes scoped to companies

**MVP:** Standardized offboarding process ensures consistent exit experience and compliance.

#### 2. Offboarding Stages
- **Stage Management:** Create offboarding stages
- **Stage Types:** Notice Period, Exit Interview, Work Handover, FnF Settlement, Farewell, Archived
- **Stage Managers:** Assign managers to stages
- **Sequence Control:** Order stages in offboarding process
- **Automatic Stage Creation:** System creates default stages

**MVP:** Stage-based offboarding ensures all exit tasks are completed systematically.

#### 3. Offboarding Tasks
- **Task Creation:** Define tasks for each stage
- **Task Managers:** Assign responsible managers
- **Stage Assignment:** Link tasks to stages
- **Task Status:** Todo, In Progress, Stuck, Completed
- **Task Description:** Detailed task information

**MVP:** Task-based offboarding checklist ensures no critical exit tasks are missed.

#### 4. Employee Offboarding
- **Employee Assignment:** Add employees to offboarding
- **Stage Tracking:** Track employee progress through stages
- **Notice Period:** Configure notice period (days/months)
- **Notice Period Dates:** Track notice period start and end
- **Automatic Calculation:** Calculate notice period automatically

**MVP:** Automated notice period tracking ensures compliance with employment contracts.

#### 5. Resignation Letters
- **Resignation Requests:** Employee-initiated resignation requests
- **Planned Leave Date:** Employee's intended last working day
- **Description:** Resignation reason and details
- **Status Tracking:** Requested, Approved, Rejected
- **Approval Workflow:** Manager approval process
- **Automatic Offboarding:** Convert approved resignations to offboarding

**MVP:** Self-service resignation requests streamline exit process initiation.

#### 6. Exit Reasons
- **Reason Tracking:** Document exit reasons
- **Reason Description:** Detailed exit information
- **Attachment Support:** Attach supporting documents

**MVP:** Exit reason tracking provides insights for retention strategies.

#### 7. Offboarding Notes
- **Note Management:** Add notes to offboarding process
- **Note Attachments:** Attach files to notes
- **Note By:** Track who added the note
- **Stage Association:** Link notes to stages

**MVP:** Comprehensive note-taking ensures knowledge transfer and process documentation.

#### 8. General Settings
- **Resignation Request:** Enable/disable resignation request feature

**MVP:** Configurable settings adapt offboarding to organizational policies.

---

## Helpdesk

**Purpose:** Internal helpdesk system for employee support and issue resolution.

### Core Features

#### 1. Ticket Management
- **Ticket Creation:** Employees create support tickets
- **Ticket Types:** Suggestion, Complaint, Service Request, Meeting Request, Anonymous Complaint, Others
- **Ticket Prefix:** Custom prefixes for ticket numbering
- **Priority Levels:** Low, Medium, High
- **Status Tracking:** New, In Progress, On Hold, Resolved, Canceled
- **Ticket Description:** Detailed issue description
- **Deadline Management:** Set resolution deadlines
- **Tag Management:** Categorize tickets with tags
- **Created Date:** Track ticket creation date
- **Resolved Date:** Track resolution date

**MVP:** Centralized ticket management provides visibility into support requests and ensures timely resolution.

#### 2. Ticket Assignment
- **Assignment Types:** Department-based, Job Position-based, Individual
- **Forward To:** Forward tickets to departments, positions, or individuals
- **Assigned To:** Assign tickets to specific employees
- **Claim Requests:** Employees can claim tickets
- **Approval Workflow:** Manager approval for ticket claims

**MVP:** Flexible assignment system ensures tickets reach the right people efficiently.

#### 3. Department Managers
- **Manager Assignment:** Assign managers to departments
- **Auto-Assignment:** Automatic ticket assignment to department managers
- **Validation:** Ensure managers belong to assigned departments

**MVP:** Department-based assignment streamlines ticket routing and reduces manual assignment.

#### 4. Comments & Attachments
- **Comment Thread:** Discussion thread on tickets
- **Comment Attachments:** Attach files to comments
- **Comment History:** Track comment history
- **File Format Detection:** Automatic format detection (image, audio, file)
- **Ticket Attachments:** Attach files directly to tickets

**MVP:** Rich communication features enable effective issue resolution and documentation.

#### 5. FAQ System
- **FAQ Categories:** Organize FAQs by categories
- **FAQ Management:** Create and manage FAQs
- **Question & Answer:** Detailed Q&A content
- **Tag Support:** Tag FAQs for easy search
- **Company-Specific:** FAQs scoped to companies

**MVP:** Self-service FAQ system reduces support ticket volume and improves employee experience.

---

## Project Management

**Purpose:** Project and task management with time tracking capabilities.

### Core Features

#### 1. Project Management
- **Project Creation:** Create projects with details
- **Project Status:** New, In Progress, Completed, On Hold, Cancelled, Expired
- **Start/End Dates:** Define project timeline
- **Project Managers:** Assign project managers
- **Project Members:** Assign project team members
- **Project Description:** Detailed project information
- **Document Attachments:** Attach project documents
- **Company-Specific:** Projects scoped to companies

**MVP:** Centralized project management provides visibility into project status and resource allocation.

#### 2. Project Stages
- **Stage Management:** Create custom project stages
- **Stage Sequence:** Order stages in project workflow
- **End Stage:** Mark stages as completion stages
- **Automatic Creation:** System creates default "Todo" stage
- **Stage Validation:** Ensure only one end stage per project

**MVP:** Stage-based project management enables Kanban-style workflow visualization.

#### 3. Task Management
- **Task Creation:** Create tasks within projects
- **Task Status:** To Do, In Progress, Completed, Expired
- **Stage Assignment:** Assign tasks to project stages
- **Task Managers:** Assign task managers
- **Task Members:** Assign task team members
- **Start/End Dates:** Define task timeline
- **Task Description:** Detailed task information
- **Document Attachments:** Attach task documents
- **Sequence Management:** Order tasks within stages
- **Date Validation:** Ensure task dates within project dates

**MVP:** Task-level management provides granular control over project execution.

#### 4. Time Sheet Management
- **Time Entry:** Employees log time spent on projects/tasks
- **Project Association:** Link time entries to projects
- **Task Association:** Link time entries to tasks
- **Date Selection:** Select date for time entry
- **Hours Spent:** Record hours worked (HH:MM format)
- **Description:** Detailed work description
- **Status Tracking:** In Progress, Completed
- **Employee Validation:** Ensure employees are project/task members
- **Date Validation:** Prevent future date entries

**MVP:** Time tracking provides accurate project costing and resource utilization insights.

#### 5. Project Dashboard
- **Project Overview:** Visual project status dashboard
- **Task Statistics:** Task count and status breakdown
- **Member Overview:** Team member assignment view

**MVP:** Dashboard view provides quick insights into project health and progress.

---

## Biometric Integration

**Purpose:** Integration with biometric devices for automated attendance tracking.

### Core Features

#### 1. Biometric Device Management
- **Device Types:** ZKTeco/eSSL, Anviz, Matrix COSEC, Dahua, e-Time Office
- **Device Configuration:** IP address, port, credentials
- **Device Direction:** In Device, Out Device, Alternate, System Direction
- **Live Status:** Real-time device connection status
- **Scheduler Configuration:** Automatic attendance fetch scheduling
- **Scheduler Duration:** Configure fetch frequency
- **Last Fetch Tracking:** Track last successful fetch date/time
- **API Integration:** API-based device integration (Anviz, e-Time Office)
- **Token Management:** API token management for cloud devices

**MVP:** Multi-device support enables integration with existing biometric infrastructure without hardware replacement.

#### 2. Employee-Device Mapping
- **User ID Mapping:** Map employees to device user IDs
- **UID Management:** Manage device-specific UIDs
- **Reference User ID:** Device reference IDs
- **Card Number:** Dahua card number mapping
- **Multi-Device Support:** Map employees to multiple devices

**MVP:** Flexible employee-device mapping supports various device configurations and employee mobility.

#### 3. Attendance Fetching
- **Automatic Fetching:** Scheduled automatic attendance data fetching
- **Manual Fetching:** On-demand attendance data retrieval
- **Fetch History:** Track fetch operations
- **COSEC Arguments:** Special handling for COSEC device arguments
- **Roll-Over Count:** Track COSEC roll-over counts
- **Sequence Numbers:** Track COSEC sequence numbers

**MVP:** Automated attendance fetching eliminates manual data entry and ensures real-time attendance tracking.

#### 4. IP-Based Access Control
- **IP Whitelist:** Restrict check-in to specific IP addresses
- **IP Range Support:** Support for IP address ranges
- **Network Validation:** Validate employee location during check-in

**MVP:** IP-based access control ensures attendance is recorded from authorized locations.

---

## Additional Features

### 1. MyHRMS Automations
- **Workflow Automation:** Automate business processes
- **Model-Based Triggers:** Trigger automations on model changes
- **Condition-Based Actions:** Execute actions based on conditions
- **Email Automation:** Automated email notifications
- **Multi-Model Support:** Support for various HR models

**MVP:** Automation reduces manual work and ensures consistent process execution.

### 2. MyHRMS API
- **RESTful API:** Comprehensive REST API for system integration
- **Authentication:** Secure API authentication
- **Data Access:** Programmatic access to HR data
- **Third-Party Integration:** Enable integration with other systems

**MVP:** API enables integration with external systems and custom applications.

### 3. MyHRMS Audit
- **Change Tracking:** Complete audit trail of all changes
- **History View:** View historical data changes
- **User Tracking:** Track who made changes
- **Timestamp Tracking:** Track when changes were made
- **Field-Level Tracking:** Track changes at field level

**MVP:** Complete audit trail ensures compliance and provides change history for troubleshooting.

### 4. MyHRMS Documents
- **Document Management:** Centralized document storage
- **Document Versioning:** Track document versions
- **Access Control:** Control document access

**MVP:** Centralized document management ensures document security and accessibility.

### 5. MyHRMS Backup
- **Data Backup:** Automated data backup
- **Backup Scheduling:** Schedule regular backups
- **Restore Capability:** Restore from backups

**MVP:** Automated backup ensures data safety and business continuity.

### 6. MyHRMS Widgets
- **Custom Widgets:** Reusable UI components
- **Dashboard Widgets:** Customizable dashboard widgets

**MVP:** Widget system enables flexible UI customization and dashboard personalization.

### 7. MyHRMS Views
- **Custom Views:** Reusable view components
- **View Templates:** Standardized view templates

**MVP:** View system ensures consistent UI/UX across the application.

### 8. Notifications
- **Real-Time Notifications:** In-app notifications
- **Email Notifications:** Email-based notifications
- **Notification Types:** Various notification types
- **Notification Preferences:** User-configurable preferences

**MVP:** Multi-channel notifications ensure important updates are never missed.

### 9. Dynamic Fields
- **Custom Fields:** Add custom fields to models
- **Field Types:** Various field types supported
- **Model Extension:** Extend existing models without code changes

**MVP:** Dynamic fields enable customization without code modifications.

### 10. Multi-Language Support
- **Internationalization:** Support for multiple languages
- **Translation Management:** Manage translations
- **Locale Support:** Support for various locales

**MVP:** Multi-language support enables global deployment and user accessibility.

### 11. Company Management
- **Multi-Tenant:** Complete data isolation between companies
- **Company Switching:** Easy switching between companies
- **Company-Specific Settings:** Settings per company
- **Headquarter Company:** Designate headquarter company

**MVP:** Multi-tenant architecture enables SaaS deployment and multi-company management.

### 12. User Management & Permissions
- **Role-Based Access:** Role-based permission system
- **Permission Management:** Granular permission control
- **User Groups:** Organize users into groups
- **Permission Inheritance:** Hierarchical permission inheritance

**MVP:** Flexible permission system ensures data security and access control.

### 13. Reporting & Analytics
- **Custom Reports:** Generate custom reports
- **Dashboard Analytics:** Visual analytics on dashboards
- **Export Capabilities:** Export data to various formats
- **Scheduled Reports:** Schedule automatic report generation

**MVP:** Comprehensive reporting enables data-driven decision making.

### 14. Email System
- **Email Templates:** Reusable email templates
- **Dynamic Configuration:** Dynamic email server configuration
- **Email Logging:** Track all sent emails
- **Template Variables:** Dynamic content in templates

**MVP:** Flexible email system ensures reliable communication with employees and candidates.

### 15. Announcements
- **Company Announcements:** Broadcast announcements to employees
- **Expiration Dates:** Set announcement expiration
- **Target Audience:** Company-wide or specific groups
- **Comment System:** Employee comments on announcements
- **View Tracking:** Track who viewed announcements

**MVP:** Centralized announcement system ensures important information reaches all employees.

---

## Technical Architecture

### Database Schema
- **PostgreSQL:** Primary database (recommended)
- **Multi-Tenant Design:** Company-based data isolation
- **Audit Logging:** Complete change history
- **Soft Deletes:** Archive instead of delete
- **Indexing:** Optimized database indexes

### Security Features
- **XSS Protection:** Input sanitization
- **CSRF Protection:** Cross-site request forgery protection
- **SQL Injection Prevention:** Parameterized queries
- **File Upload Validation:** Secure file handling
- **Password Security:** Secure password storage

### Performance Optimizations
- **Query Optimization:** Efficient database queries
- **Caching:** Strategic caching implementation
- **Lazy Loading:** Optimized data loading
- **Bulk Operations:** Batch processing support

### Integration Capabilities
- **REST API:** Comprehensive API for integration
- **Webhook Support:** Event-driven integrations
- **Third-Party Integrations:** LinkedIn, biometric devices
- **Import/Export:** Data import and export capabilities

---

## Conclusion

MyHRMS  provides a comprehensive, feature-rich solution for human resource management. With its modular architecture, flexible configuration options, and extensive feature set, it caters to organizations of all sizes. The system's emphasis on automation, compliance, and user experience makes it an ideal choice for modern HR departments seeking to streamline operations and improve efficiency.

**Key Strengths:**
- Complete HR lifecycle management
- Flexible configuration and customization
- Multi-tenant architecture
- Comprehensive audit trails
- Integration capabilities
- Open-source and extensible

**Ideal For:**
- Small to large enterprises
- Multi-company organizations
- Organizations requiring compliance tracking
- Companies seeking automation
- Businesses needing customizable HR solutions

