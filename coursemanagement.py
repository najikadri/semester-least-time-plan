"""
@author: Mohammad Naji Kadri

This program creates a schedule for students with
least time gap between courses and less days in university
leaving space for the student to have an organized schedule
and more free time during the day by preventing wasted breaks

This program is not only useful but also a method to practice
CMPS200 course since it needs most of the covered materials
to be able to create such complex program
"""
import datetime
import powerset
import random
import csv

class Time:
    """
    A customized time class that contains useful methods and
    suitable representation for our courses periods
    """

    def __init__(self, string):
        """creates a time instance from given string of format %H:%M"""
        self.time = self.format_time(string)
        self.string = string # used for string representation

    def format_time(self, string):
        """
        format_time(string) -> datetime.datetime\n
        creates a datetime instance from string with 
        form %H:%M where %H is the hours value and
        %M is the minutes value
        """
        hours, minutes = string.split(':')
        hours, minutes = int(hours), int(minutes)
        # the year, month, and day is arbitrary since they are irrelevant
        return datetime.datetime(2018, 1, 4, hours, minutes)

    def __sub__(self, other):
        """returns the duration between two times in minutes"""
        return ((self.time - other.time).total_seconds())/60

    def __lt__(self, other):
        """compare two times by their values"""
        return self.time < other.time

    def __str__(self):
        """returns the string format of the time instance"""
        return self.string

    def __repr__(self):
        """returns the string representation of the time instance"""
        return f'<Time: {self.string}>'

class Day:
    """
    a class to represent days and its formatting appropriate
    for the courses
    """

    # mapping of day abbreviations to their full names

    days = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'R': 'Thursday',
    'F': 'Friday'
    }

    week = ['M','T','W','R','F'] # days of the week 

    def __init__(self, abrv):
        """creates Day instance from day abbreviation"""
        self.full_name = self.full_day(abrv)
        self.abbreviation = abrv

    @staticmethod
    def full_day(abrv):
        """returns the day's full name"""
        return Day.days[abrv]

    @staticmethod
    def format_days(string):
        """format a string of days (i.e  'MWF') and returns a list of days"""
        days_list = []
        for day in Day.days:
            if day in string:
                days_list.append(Day(day))
        return days_list

    def __str__(self):
        """returns the day's full name for printing"""
        return self.full_name

    def __repr__(self):
        """returns the representation of the day"""
        return f'{self.abbreviation}: {self.full_name}'

def booleanize(string):
    """makes a boolean out of a string"""
    if string.lower() == 'true':
        return True
    else:
        return False

class Course:
    """
    The Course Class contains all the necessary information for
    presenting a course and its attributes
    """

    def __init__(self, name, section, ctype, crn, days, starts, ends, linked_crns, link_required):
        """create a Course instance and make sure all the necessary information is present (must be in form of  strings)"""
        self.name = name
        self.section = section
        self.course_type = ctype
        self.crn = int(crn)
        self.days = Day.format_days(days)
        self.daysabrv = days 
        self.starts = Time(starts)
        self.ends = Time(ends)
        self.linked_crns = Course.format_crns(linked_crns)
        self.link_required = booleanize(link_required)

    @staticmethod
    def format_crns(string):
        """
        creates a list of crns delimited by - (hyphen)\n
        example: format_crns('12345-1468') -> [12345, 1468]
        """
        if string == '' or string == ' ':
            return []
        else:
            crns = string.split('-')
            crns = [int(crn) for crn in crns]
            return crns

    # here we have some getters methods

    def get_name(self):
        return self.name

    def get_section(self):
        return self.section

    def get_course_type(self):
        return self.course_type

    def get_crn(self):
        return self.crn

    def get_days(self):
        return self.daysabrv

    def get_days_list(self):
        return self.days

    def has_required_link(self):
        return self.link_required

    def get_linked_crns(self):
        return self.linked_crns

    def get_starting_time(self):
        return self.starts

    def get_ending_time(self):
        return self.ends

    def get_duration(self):
        return self.ends - self.starts

    def __sub__(self, other):
        """calculates the time difference (gap) between two courses"""
        return self.starts - other.ends # time from the first course end time to the start of the next one

    def __eq__(self, other):
        """two courses are equal if they have the same name and same type"""
        try:
            return (self.name == other.name and self.course_type == other.course_type) \
            or self.get_crn() == other.get_crn()
        except:
            return False

    def __str__(self):
        """returns a string containing main info about the course"""
        return f'course name: {self.name}, Section: {self.section}, CRN: {str(self.crn)}'

    def __repr__(self):
        """returns a string representation of the course"""
        return f'<Course: {self.name} - {self.section}, CRN: {str(self.crn)}>'


class CourseNotFoundException(Exception):
    """
    Exception raised when a course or its CRN is
    missing from the list of available courses (search scope)
    """
    pass

class CourseManager:
    """
    The CourseManager class contains all the methods
    needed to manage courses and semesters
    """

    def __init__(self, student_name, semester_name, courses_csv):
        """loads a courses of a specific semester to manage it"""
        self.student_name = student_name
        self.semester_name = semester_name
        self.available_courses = CourseManager.load_courses(courses_csv)
        self.courses_dict = self.build_courses_dict()

    @staticmethod
    def load_courses(csv_file):
        """return a list of courses loaded from a csv file"""
        courses = []
        with open(csv_file) as csv_file:
            data = csv.reader(csv_file, delimiter = ',')
            line = 0
            for row in data:
                if line == 0:
                    line += 1
                    continue
                else:
                    courses.append(Course(*row)) # unpack the elements of the row as arguments
                line += 1
        return courses

    @staticmethod
    def view_courses(courses):
        """listing of the courses given"""
        c = 1
        for course in courses:
            print(c,'-',course)
            c += 1


    # getter methods

    def get_available_courses(self):
        return self.available_courses

    def get_student_name(self):
        return self.student_name

    def get_semester_name(self):
        return self.semester_name

    def get_courses_dict(self):
        return self.courses_dict

    def build_courses_dict(self):
        """
        creates a dictionary that maps CRN values to their Course instances.\n
        the dictionary is used to speed up searching a course in the available
        courses of the current semester.
        """
        crn_courses = {}
        for course in self.available_courses:
            crn_courses[course.get_crn()] = course
        return crn_courses


    def overlap(self, course1, course2):
        """checks if the courses overlap where course1 must be before course2"""
        return course2 - course1 <= 0

    def conflict(self, courses):
        """checks if there is any overlap between two consecutive courses (given they are sorted)"""
        for i in range(1,len(courses)):
            if self.overlap(courses[i - 1], courses[i]):
                return True
        return False

    def select_course(self, name):
        """returns a list of course sections with provided coursse name"""
        courses = []
        for course in self.available_courses:
            if course.name.lower() == name.lower() or \
            ''.join(course.name.split()).lower() == name.lower(): # (i.e. cmps211 returns true (matches) for CMPS 211 course)
                courses.append(course)
        if courses == []:
            raise CourseNotFoundException(f'{name} course is missing or not part of the system!')
        return courses

    def select_courses(self, course_names):
        """returns all courses of given list of course names"""
        courses = []
        for name in course_names:
            courses.extend(self.select_course(name))
        return courses

    def crn_to_course(self, crn):
        """returns the course instance that has a given CRN, -1 if not found"""
        try:
            return self.courses_dict[crn]
        except KeyError:
            return -1

    def crns_to_courses(self, crns):
        """returns a list of courses that have the CRNs provided by the user"""
        courses = []
        for crn in crns:
            course = self.crn_to_course(crn)
            if course == -1:
                raise CourseNotFoundException(f'{str(crn)} is missing or incorrect!')
            else:
                courses.append(course)
        return courses

    def requirements_met(self, selected_courses, course):
        """checks if a course's requirements has been met in the selected courses"""
        if course not in selected_courses: # course must be in the semester plan
            return False
        elif not course.has_required_link() or course.get_linked_crns() == []:
            return True # if there are no linked courses then requirements are met
        else:
            links = course.get_linked_crns()
            already_found = False
            # check that only one linked CRN is in the semster plan
            for c in selected_courses:
                if c.get_crn() in links:
                    if not already_found:
                        already_found = True
                    else:
                        return False
            return already_found

    def create_semester_plan(self, selected_courses):
        """creates a semester plan by week from selected courses"""
        plan = {day:[] for day in Day.week} #make a key of each day and give each key an empty list
        for course in selected_courses:
            for day in course.get_days_list():
                plan[day.abbreviation].append(course)

        # sort the courses for each day by their ending time

        for day in plan:
            self.sort_courses(plan[day])
        return plan

    def sort_courses(self, courses):
        """sort courses in a list by their ending time"""
        courses.sort(key = lambda x: x.get_ending_time())

    def view_plan(self, semester_plan):
        """a way to visualize and pretty print the semester plan"""
        days = Day.week
        for day in days:
            if len(semester_plan[day]) == 0:
                print(f'{Day.full_day(day)}:\n\t no course is taken at this day\n')
            else:
                print(f'{Day.full_day(day)}:')
                self.view_courses(semester_plan[day])
                print()


    def view_plans(self, semester_plans):
        """view a list of semester plans to compare between them"""
        p = 1
        for plan in semester_plans:
            print('Semester Plan',p)
            print()
            self.view_plan(plan)
            print('#' * 50)
            p += 1

    def contains_equiv(self, selected_courses):
        """checks if there are any equivalent courses in the list"""
        for course1 in selected_courses:
            for course2 in selected_courses:
                if course1.get_crn() != course2.get_crn() and \
                course1 == course2:
                    return True
        return False

    def daytime_break(self, courses):
        """returns the total break duration between courses in a day"""
        total_break = 0
        for i in range(1,len(courses)):
            total_break += courses[i] - courses[i - 1] # calculates time difference in minutes
        return total_break

    def plan_total_breaks(self, semester_plan):
        """returns the total number of earned breaks (time gaps) for the semester plan"""
        total_time = 0
        for day in Day.week:
            total_time += self.daytime_break(semester_plan[day])
        return total_time

    def contains_courses(self, selected_courses, course_names):
        """returns true if every course subject is found in the list of selected courses"""
        courses = [self.select_course(course_name) for course_name in course_names]
        for course in courses:
            course_found = False
            for section in course:
                if section in selected_courses and section.get_course_type() == 'lecture':
                    course_found = True
            if not course_found:
                return False
        return True

    def valid_semester(self, selected_courses, semester_plan):
        """
        this validate if the semester plan is acceptable or not by
        checking if each course has its required linked courses and
        that there is no time conflict between any time.
        """
        all_met = all([self.requirements_met(selected_courses,course) for course in selected_courses])
        conflicted = any([self.conflict(semester_plan[day]) for day in Day.week])
        has_equivalent_courses = self.contains_equiv(selected_courses)
        return all_met and not conflicted and not has_equivalent_courses

    def bf(self, course_names):
        """
        This method uses the brute force technique to find the optimal solution which
        is finding the semester plan with the least time gap between each course and is valid.
        This is done by selecting the courses sections that are required by the student and try
        different combinations. Then we select only the valid semester plans.
        from these we calculate the sum of time gap for each day and return the semester plan with
        least time gaps possible.
        The method returns a 2-tuple having the semester plan and its selected courses list
        """
        possible_courses = self.select_courses(course_names)
        possible_plans = [(course_combo, self.create_semester_plan(course_combo)) for course_combo in powerset.generatePowerSet(possible_courses)]
        valid_plans = [plan for plan in possible_plans if self.valid_semester(plan[0],plan[1]) and self.contains_courses(plan[0],course_names)]
        plans_breaks = [self.plan_total_breaks(plan[1]) for plan in valid_plans]
        optimal_plan = valid_plans[plans_breaks.index(min(plans_breaks))] # this is our optimal semester_plan
        return optimal_plan


    def greedy_time(self, course_names, semester_plan):
        """
        This technique try to create a semester plan that finishes early.
        For each course we select the ones with the earliest time given
        and we select a linked course at the earliest time possible
        and we make sure that our new selections do not conflict with 
        the other courses already selected.
        This is done recursively for each course name
        """
        if len(course_names) == 1:
            self.inject_course(course_names[0], semester_plan)
        else:
            n = len(course_names)//2
            left = course_names[:n]
            right = course_names[n:]
            self.greedy_time(left,semester_plan)
            self.greedy_time(right,semester_plan)

    def inject_course(self, course_name, semester_plan):
        """helper method for the time greedy algorithm."""
        courses = self.select_course(course_name) # get that one course subject
        lectures = [course for course in courses if course.get_course_type() == 'lecture'] # find all the lectures

        earliest = None
        course_works = False
        if not lectures[0].has_required_link(): # check if the course requires a link
            while not course_works:
                earliest = min(lectures, key = lambda x: x.get_starting_time()) # find the earliest lecture available

                # add the lecture to the current semester plan

                new_semester = semester_plan[0] + [earliest]

                new_plan = self.create_semester_plan(new_semester)

                semester_plan[1] = self.create_semester_plan(semester_plan[0])

                # check if the semester_plan is still working
                if self.valid_semester(new_semester,new_plan):
                    course_works = True # the lecture selected works
                    semester_plan[0] = new_semester
                    semester_plan[1] = new_plan
                    return
                else:
                    lectures.pop(lectures.index(earliest)) # we can't use it so we remove it from the suggestions
        else: # the lecture requires linked courses then
            while not course_works:
                earliest = min(lectures, key = lambda x: x.get_starting_time()) # find the earliest lecture available
                temp_link = self.crn_to_course(earliest.get_linked_crns()[0]) # use a temporary link to make course valid 
                # add the lecture a new semester plan
                new_semester = semester_plan[0] + [earliest,temp_link]
                new_plan = self.create_semester_plan(new_semester)
                # check if the semester_plan is still working
                if self.valid_semester(new_semester,new_plan):
                    course_works = True # the lecture selected works
                    semester_plan[0] = semester_plan[0] + [earliest]
                    semester_plan[1] = self.create_semester_plan(semester_plan[0])
                else:
                    lectures.pop(lectures.index(earliest)) # we can't use it so we remove it from the suggestions

            # after we removed the temporary link, now find the early one using the same technique for finding the right lecture
            link_found = False
            early_link = None
            links = self.crns_to_courses(earliest.get_linked_crns())
            while not link_found:
                early_link = min(links, key = lambda x: x.get_starting_time()) 
                
                new_semester = semester_plan[0] + [early_link]
                new_plan = self.create_semester_plan(new_semester)

                if self.valid_semester(new_semester,new_plan):
                    link_found = True
                    semester_plan[0] = new_semester
                    semester_plan[1] = new_plan
                else:
                     links.pop(links.index(early_link))

    def greedy(self, course_names):
        """
        finds a good solution for saving time by using greedy algorithm.
        it doesn't give the optimal solution but a very convenient one or
        a very similar one.

        for some reason this method doesn't work when 
        the courses with linked section are at the end of
        the list and I don't have the brain power to fix
        it now so make sure to place these first before
        courses who don't require any linked sections.
        The problem I have observed isn't because it is linked
        but because we always choose the earliest one we 
        encounter a situation when the algorithm tries to
        find an early time that is already taken by the other
        courses. That would change the whole code or else it 
        won't work.
        A working solution is to shuffle the course_names list 
        to obtain new ordering and hope it works
        Even though it works it is not efficient
        """
        s = [[],self.create_semester_plan([])]
        try:
            self.greedy_time(course_names, s)
            return s
        except ValueError:
            random.shuffle(course_names)
            return self.greedy(course_names)


    def __getitem__(self, idx):
        """returns a course from the available courses"""
        return self.available_courses[idx]

    def __len__(self):
        """returns the number of available courses of the current semester"""
        return len(self.available_courses)

    def __str__(self):
        """returns a string with info about the course manager"""
        return f"{self.student_name}'s CourseManager for {self.semester_name} ({str(len(self))})'"

    def __repr__(self):
        """returns a representation of the course manager"""
        return f'<CourseManager: {self.semester_name}, {self.student_name}>'


# shortcut for the CourseManager's view_courses() static method
view = lambda x: CourseManager.view_courses(x)

if __name__ == '__main__':

    c = CourseManager('Mohammad Kadri', 'Fall 18-19', 'fall18-19.csv')

    # plan = c.bf(['cmps211','engl203'])


    # k = c.crns_to_courses([312210, 112440, 112441, 126801])

    # p = c.create_semester_plan(k)

    # print(c.valid_semester(k,p))

    s = c.greedy(['cmps211', 'engl203', 'math201'])

    # s = c.greedy(['math201', 'engl203', 'cmps211'])

    c.view_plan(s[1])

    print('#' * 50)

    p = c.bf(['cmps211', 'engl203', 'math201'])

    # p = c.bf(['math201', 'engl203', 'cmps211'])

    c.view_plan(p[1])

    # c.view_plan(plan[1])

    # c.view_plans([combo[1] for combo in plans])


