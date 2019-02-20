import re

output_file = open('C:\\Users\\admin\\Desktop\\experimenter_platform_core\\ATUAV_Experimenter_Platform\\database\updated_rule_noremoval.csv', 'w')

with open('C:\\Users\\admin\\Desktop\\experimenter_platform_core\\ATUAV_Experimenter_Platform\\database\\rule_removal.old.csv', 'r') as rule_file:
    for l in rule_file:
        new_l = re.sub("select case when count\(\*\) > ([0-9]+)", lambda m: 'select case when count(*) > '+str(int(int(m.group(1)) * 0.7)), l)
        output_file.write(new_l)

output_file.close()
