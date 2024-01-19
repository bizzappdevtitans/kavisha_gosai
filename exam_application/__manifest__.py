{
    "name": "Examination Application",
    "summary": "USe for Examination Purpose",
    "author": "BizzAppDev",
    "website": "https://bizzappdev.com",
    "version": "15.0.1.0.0",
    "depends": ["base","mail"],
    "license": "LGPL-3",
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/student_details_views.xml",
        "views/subject_details_views.xml",
        "views/teachers_details_views.xml",
        "views/exam_menu_views.xml",
    ],
}
