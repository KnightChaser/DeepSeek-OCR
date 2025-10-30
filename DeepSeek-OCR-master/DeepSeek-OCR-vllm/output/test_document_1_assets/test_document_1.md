
# CURLY SPIDER  


CrowdStrike OverWatch in Action: Stopping a Social Engineering Attack in Under 4 Minutes  

![Figure 1](test_document_1_img1.png)


<center>Figure 5. Timeline of CrowdStrike OverWatch moving faster than CURLY SPIDER to stop a social engineering attack in less than four minutes </center>  


Once CURLY SPIDER gains initial access, their window of opportunity is limited - - access will only last as long as the victim remains on the call. To extend control, the adversary's immediate objective is to establish persistent access before the session ends.  


With remote access secured, CURLY SPIDER moves quickly - - often while still actively engaging with the victim - - to deploy their payloads and establish persistence. The bulk of the intrusion time is spent ensuring connectivity and troubleshooting any access issues to reach their cloud- hosted malicious scripts.  


## 1. Validating Connectivity (3:43)  


- Posing as IT support offering assistance, the adversary requests access to Quick Assist.- The adversary ensures a connection to pre-configured cloud storage, where they host malicious scripts and work through any access barriers. Once access is confirmed, CURLY SPIDER downloads malicious scripts.  


## 2. Deploying Payload (0:06)  


- CURLY SPIDER executes the scripts via curl or PowerShell. These scripts:- Modify registry run keys, creating a user to ensure execution at startup- Remove forensic artifacts to erase traces of the intrusion  


## 3. Establishing Persistent Access (0:06)  


- The adversary creates a backdoor user, embedding persistence directly into the system.- The final payload is executed under a legitimate binary, allowing CURLY SPIDER to blend into normal activity and evade detection.  


In this example, CURLY SPIDER does not rely on traditional "breakout" techniques to move laterally. Instead, the adversary compromises the network in seconds by securing long- term access before the victim even realizes what's happening.