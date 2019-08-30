#!/usr/bin/env

#reads the file in a list
with open('jobs.txt', 'r') as f:
    job_list = (f.readlines())

#removes the newlines & underscores from the list
job_list = [ word.replace('_',' ').strip('\n') for word in job_list ]
print(job_list)

#fixable words
job_list = [ word.replace('cardiologist', 'cardiology cardiologist').replace('crooner','croon crooner').replace('dermatologist','dermatology dermatologist').replace('epidemiologist', 'epidemiology epidemiologist').replace('financier','finance financier').replace('mediator','mediate mediator').replace('negotiator','negotiate negotiator').replace('neurologist','neurology neurologist').replace('pathologist','pathology pathologist').replace('pharmacist','pharmacy pharmacist').replace('photojournalist', 'photo journal journalist').replace('radiologist', 'radiology radiologist').replace('strategist','strategy strategist').replace('stylist','style stylist').replace('stockbroker','stock broker').replace('paralegal', 'para legal').replace('plumber', 'plumbing plumber').replace('realtor','real estate realtor').replace('restaurateur','restaurant restaurateur').replace('understudy','under study') for word in job_list]

del_words = ['artiste', 'custodian', 'janitor', 'pundit', 'hairdresser', 'valedictorian', 'welder', 'tycoon', 'undersecretary']

for word in del_words:
   job_list.remove(word) 

print("NEW LIST:\n")
for i in range(len(job_list)):
        print("item ",i+1, job_list[i])
        if (i+1)%10 == 0:
            print("\n")

print(job_list)

with open('fixed_jobs.txt','w') as f:
    for job in job_list:
        f.write('%s\n' % job)
