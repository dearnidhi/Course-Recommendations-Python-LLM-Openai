# from db import get_database_connection

# def get_course_recommendations(searched_semester):
#     db = get_database_connection()

#     # List of collections in the order of semesters
#     collections = ['1st_sem', '2nd_sem', '3rd_sem', '4th_sem', '9th_sem', '10th_sem']

#     # Find the index of the searched semester and recommend the following semesters
#     try:
#         index = collections.index(searched_semester)
#     except ValueError:
#         return []

#     recommended_collections = collections[index+1:]

#     recommended_courses = []
#     for collection in recommended_collections:
#         courses = db[collection].find()
#         for course in courses:
#             recommended_courses.append(course)
    
#     return recommended_courses


from db import get_database_connection

def get_course_recommendations(searched_semester_name):
    db = get_database_connection()

    # Dictionary with keys as the user-friendly semester names and values as the collection names
    semester_to_collection_mapping = {
        'Semester 1': '1st_sem',
        'Semester 2': '2nd_sem',
        'Semester 3': '3rd_sem',
        'Semester 4': '4th_sem',
        'Semester 9': '9th_sem',
        'Semester 10': '10th_sem'
    }

    # Check if the searched semester is in the mapping
    if searched_semester_name not in semester_to_collection_mapping:
        return []

    searched_collection = semester_to_collection_mapping[searched_semester_name]

    collections = list(semester_to_collection_mapping.values())
    index = collections.index(searched_collection)
    recommended_collections = collections[index+1:]

    recommended_courses = []
    for collection in recommended_collections:
        courses = db[collection].find()
        for course in courses:
            recommended_courses.append(course)

    return recommended_courses

