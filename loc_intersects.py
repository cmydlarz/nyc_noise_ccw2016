import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import urllib
import json
import sys

# input_file = sys.argv[1]

# API url to retrieve shapefile data for census tracts in JSON format
tract_link = 'http://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/nyct2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=geojson'

# Retrieve shapefile data
f = urllib.urlopen(tract_link)           
tract_str = f.read()

# Set start time-date and comaplint type substring for 311 complaint data retrievel (only returning DEP handled complaints)
timeanddate = '2015-08-29T12:00:00'
searchstr = 'Noise'

# API url to retrieve 311 complaint data in JSON format
noise_link = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$$app_token=Gxk5zCqWzCRJTJ5ox9CaFrVP9&$where=starts_with(complaint_type, "' + searchstr + '") and created_date > "' + timeanddate + '" and latitude IS NOT NULL and agency = "DEP"&$select=created_date,closed_date,agency,agency_name,complaint_type,descriptor,location_type,incident_zip,city,borough,status,due_date,latitude,longitude'

# Retrieve complaint data
f = urllib.urlopen(noise_link)        
noise_str = f.read()

# Convert API response strings to JSON objects
tract_data = json.loads(tract_str)
complaint_data = json.loads(noise_str)


print '311 complaints returned: ' + str(len(complaint_data))

# Output tract level CSV setup
filename = 'tract_data.csv'
out_file = open(filename, 'w')
out_file.write('tract_num,tract_code,boro_code,boro_string,nta_code,nta_string,puma_code,count')
out_file.write('\n')

# Progress display setup
total_tracts = len(tract_data['features'])
tract_cnt = 0

# Loop through each census tract and count each complaint occuring within its boundaries
for i in tract_data['features']:
	poly = i['geometry']['coordinates'][0]
	complaint_count = 0
	for complaint in complaint_data:
		complaint_loc = [complaint['latitude'], complaint['longitude']]
		if len(poly) == 1:
			for j in poly:
				bbpath = mplPath.Path(j)
				if bbpath.contains_point((float(complaint_loc[1]), float(complaint_loc[0])):
					complaint_count += 1
					
		else:
			bbpath = mplPath.Path(poly)
			if bbpath.contains_point((float(complaint_loc[1]), float(complaint_loc[0])):
				complaint_count += 1
				
	# Write out row of CSV out file with census tract data including count of complaint within each census tract
	out_file.write(i['properties']['CTLabel'] + ','+ \
		i['properties']['BoroCT2010'] + ',' + \
		i['properties']['BoroCode'] + ',' + \
		i['properties']['BoroName'] + ',' + \
		i['properties']['NTACode'] + ',' + \
		i['properties']['NTAName'] + ',' + \
		i['properties']['PUMA'] + ',' + \
		str(complaint_count))
	out_file.write('\n')
	tract_cnt += 1
	per_done = float(tract_cnt) / float(total_tracts) * 100
	print 'Percentage complete: %.2f' % per_done
	

out_file.close()