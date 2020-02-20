# Responsys Campaign Details Getter

Python script that can log into a clients Responsys account via API and pull in campaign details for specific campaigns in an array. 

It will sort and format these details into a .json file that is then posted to an AWS S3 bucket to be used by another application that displays an html template with these campaign details.