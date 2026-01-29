def gale_shapley(n, hospital_preferences, student_preferences):
    # from slides: initialize each person and hospital to be free

    hospital_pairings = [0] * (n+1)
    student_pairings = [0] * (n+1)
    next_proposal = [0] * (n+1)

    free_hospitals_stack = list(range(1, n+1))

    while free_hospitals_stack:  #some hospital is free and hasn’t been matched/assigned to every applicant)
        current_hospital = free_hospitals_stack.pop()

        # 1st applicant on h's list to whom h has not been matched
        applicant = hospital_preferences[current_hospital - 1][next_proposal[current_hospital]]
        next_proposal[current_hospital] += 1

        #if applicant is free assign hospital to applicant
        if student_pairings[applicant] == 0:
            student_pairings[applicant] = current_hospital
            hospital_pairings[current_hospital] = applicant
        else: #a prefers h to her/his current assignment h'
            assigned_hospital = student_pairings[applicant]
            
