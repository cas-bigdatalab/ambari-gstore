#!/bin/sh
url=http://$1:6188/ws/v1/timeline/metrics
hostname=$2
appid='gstorems'
monitor_file='/tmp/gstorms.monitor'
while [ 1 ]
do
rm -rf monitor_file
curl "http://$2:8006/gStorems/servlet/GStoreServlet?action=monitor&dbName=lubm&username=root&password=123456" -o $monitor_file
# content=`cat monitor`
# echo $content
# arr=(${content// / }) 
triple=`grep -Po '(?<=triplenum":)[0-9]+' $monitor_file`
# triple=`bc -l <<< "${triple}/1000000"`
entity=`grep -Po '(?<=entitynum":)[0-9]+' $monitor_file`
# entity=`bc -l <<< "${entity}/1000000"`
literal=`grep -Po '(?<=literalnum":)[0-9]+' $monitor_file`
subject=`grep -Po '(?<=subjectnum":)[0-9]+' $monitor_file`
# subject=`bc -l <<< "${subject}/1000000"`
predicate=`grep -Po '(?<=predicatenum":)[0-9]+' $monitor_file`
connection=`grep -Po '(?<=connectionnum":)[0-9]+' $monitor_file`

# echo $triple
# echo $entity
# echo $literal
# echo $subject
# echo $predicate
# echo $connection

millon_time=$(( $(date +%s%N) / 1000000 ))
json="{
 \"metrics\": [
 {
 \"metricname\": \"triple\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${triple}
 }
 },
 {
 \"metricname\": \"entity\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${entity}
 }
 },
 {
 \"metricname\": \"literal\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${literal}
 }
 },
 {
 \"metricname\": \"subject\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${subject}
 }
 },
 {
 \"metricname\": \"predicate\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${predicate}
 }
 },
 {
 \"metricname\": \"connection\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${connection}
 }
 }
 ]
}"
 
# echo $json |tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 5
done
