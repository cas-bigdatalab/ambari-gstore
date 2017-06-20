#!/bin/sh
url=http://$1:6188/ws/v1/timeline/metrics
hostname=$2
appid='gstore'
while [ 1 ]
do
rm -rf monitor
curl http://$2:9000/monitor -o monitor
content=`cat monitor`
echo $content
arr=(${content// / }) 
triple=${arr[4]}
entity=${arr[7]}
literal=${arr[10]}
subject=${arr[13]}
predicate=${arr[16]}
connection=${arr[19]}
#echo $triple
#echo $entity
#echo $literal
#echo $subject
#echo $predicate
#echo $connection

millon_time=$(( $(date +%s%N) / 1000000 ))
random=`expr $RANDOM % 10`
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
 
echo $json |tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 5
done
