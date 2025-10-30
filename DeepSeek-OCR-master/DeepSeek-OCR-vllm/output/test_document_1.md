<|ref|>title<|/ref|><|det|>[[92, 115, 300, 201]]<|/det|>
# CURLY SPIDER  

<|ref|>text<|/ref|><|det|>[[324, 152, 587, 200]]<|/det|>
CrowdStrike OverWatch in Action: Stopping a Social Engineering Attack in Under 4 Minutes  

<|ref|>image<|/ref|><|det|>[[66, 245, 930, 412]]<|/det|>
<|ref|>image_caption<|/ref|><|det|>[[62, 422, 581, 448]]<|/det|>
<center>Figure 5. Timeline of CrowdStrike OverWatch moving faster than CURLY SPIDER to stop a social engineering attack in less than four minutes </center>  

<|ref|>text<|/ref|><|det|>[[64, 473, 902, 522]]<|/det|>
Once CURLY SPIDER gains initial access, their window of opportunity is limited - - access will only last as long as the victim remains on the call. To extend control, the adversary's immediate objective is to establish persistent access before the session ends.  

<|ref|>text<|/ref|><|det|>[[64, 540, 900, 589]]<|/det|>
With remote access secured, CURLY SPIDER moves quickly - - often while still actively engaging with the victim - - to deploy their payloads and establish persistence. The bulk of the intrusion time is spent ensuring connectivity and troubleshooting any access issues to reach their cloud- hosted malicious scripts.  

<|ref|>sub_title<|/ref|><|det|>[[66, 607, 312, 622]]<|/det|>
## 1. Validating Connectivity (3:43)  

<|ref|>text<|/ref|><|det|>[[84, 633, 907, 692]]<|/det|>
- Posing as IT support offering assistance, the adversary requests access to Quick Assist.- The adversary ensures a connection to pre-configured cloud storage, where they host malicious scripts and work through any access barriers. Once access is confirmed, CURLY SPIDER downloads malicious scripts.  

<|ref|>sub_title<|/ref|><|det|>[[66, 704, 276, 719]]<|/det|>
## 2. Deploying Payload (0:06)  

<|ref|>text<|/ref|><|det|>[[84, 730, 653, 800]]<|/det|>
- CURLY SPIDER executes the scripts via curl or PowerShell. These scripts:- Modify registry run keys, creating a user to ensure execution at startup- Remove forensic artifacts to erase traces of the intrusion  

<|ref|>sub_title<|/ref|><|det|>[[66, 812, 368, 826]]<|/det|>
## 3. Establishing Persistent Access (0:06)  

<|ref|>text<|/ref|><|det|>[[84, 838, 895, 898]]<|/det|>
- The adversary creates a backdoor user, embedding persistence directly into the system.- The final payload is executed under a legitimate binary, allowing CURLY SPIDER to blend into normal activity and evade detection.  

<|ref|>text<|/ref|><|det|>[[64, 908, 848, 957]]<|/det|>
In this example, CURLY SPIDER does not rely on traditional "breakout" techniques to move laterally. Instead, the adversary compromises the network in seconds by securing long- term access before the victim even realizes what's happening.