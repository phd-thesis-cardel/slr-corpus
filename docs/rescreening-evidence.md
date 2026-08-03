---
title: Evidence for the re-screening of the systematic review corpus
author: Carlos A. Delgado S.
date: 2026-08-03
version: 1.0
status: review
tags: [slr, prisma, screening, corpus]
---

# Re-screening evidence

Every study in the corpus was judged again against the inclusion and
exclusion criteria declared in the review methodology, in particular the
two exclusion clauses that read *Publications not directly related to
RESTful API security or mutation testing* and *Articles focusing on
non-RESTful API security or unrelated mutation testing domains*.

Each proposed exclusion was then given to an independent adjudicator
instructed to rescue it if any honest reading placed the study inside the
broad bibliometric scope, which admits adjacent work on web services,
fault injection and stateful fuzzing. Studies that survived that step are
listed in the second section and remain in the corpus.

- Studies judged: **160**
- Exclusions upheld: **48**
- Proposed exclusions rescued: **9**
- Corpus after re-screening: **112**

The dominant cause is homonymy. The term *mutation operator* carries a
distinct technical meaning in evolutionary computation, where it names a
genetic operator, and *mutation* carries a third meaning in molecular
biology. Neither sense is the one this review is about.

## Exclusions upheld

### RQ1 (4 studies)

**Many-Objective Optimization-Based Task Scheduling in Hybrid Cloud Environments**  
`ID 2` · 2023 · CMES - Computer Modeling in Engineering and Sciences · 10.32604/cmes.2023.026671

*Reason.* Planificación de tareas en nube con algoritmos evolutivos; el "mutation operator" es de computación evolutiva, no testing de mutación ni seguridad de APIs.

> a many-objective hybrid cloud task scheduling optimization model (HCTSO)... a dynamic range mutation operator are designed to extend the search range".

**Preserving privacy while revealing thumbnail for content-based encrypted image retrieval in the cloud**  
`ID 3` · 2022 · Information Sciences · 10.1016/j.ins.2022.05.008

*Reason.* Cifrado y recuperación de imágenes con algoritmos genéticos; dominio ajeno al testing/seguridad de APIs y servicios web.

> a thumbnail preserving encryption (TPE) based on genetic algorithm ... through crossover and mutation operators of the genetic algorithm".

**Resource optimization of container orchestration: a case study in multi-cloud microservices-based applications**  
`ID 5` · 2018 · Journal of Supercomputing · 10.1007/s11227-018-2345-2

*Reason.* Optimización de despliegue de contenedores con NSGA-II; los operadores de mutación son genéticos, sin relación con testing ni seguridad de APIs.

> optimize the deployment of microservices-based applications using containers ... NSGA-II with a two-point crossover operator and three mutation operators".

**Cloud computing resource scheduling and leasing algorithm based on extreme price filter**  
`ID 6` · 2017 · International Journal of Reasoning-based Intelligent Systems · 10.1504/IJRIS.2017.090036

*Reason.* Planificación y arriendo de recursos en la nube por precio; mutación no uniforme de un algoritmo genético, dominio no relacionado.

> cloud computing virtual resource leasing algorithm considering about extreme price filtering ... non-uniform mutation operator has been used to make local operating adjusting".

### RQ2 (11 studies)

**A hybrid genetic-based task scheduling algorithm for cost-efficient workflow execution in heterogeneous cloud computing environment**  
`ID 18` · 2024 · Cluster Computing · 10.1007/s10586-024-04468-6

*Reason.* Planificación de workflows en la nube con algoritmo genético híbrido; sin testing ni seguridad de APIs o servicios web.

> a hybrid genetic algorithm (HGA) is presented for reliable and cost-efficient task scheduling ... new crossover and mutation operators for global search".

**NSGA-II-AMO: A Faster Genetic Algorithm for QWSCP**  
`ID 19` · 2023 · Studies in Computational Intelligence · 10.1007/978-3-031-19604-1_15

*Reason.* Optimización evolutiva de la composición de servicios web por QoS: ni testing ni seguridad, y el operador de mutación es genético.

> QoS-driven web service composition problem (QWSCP) ... uses an adaptive mutation operator to complete the mutation process when generating children in the NSGA-II algorithm".

**A Novel Multi-Objective Optimization Based Evolutionary Algorithm for Optimize the Services of Internet of Everything**  
`ID 20` · 2022 · IEEE Access · 10.1109/ACCESS.2022.3209389

*Reason.* Algoritmo evolutivo multiobjetivo para optimizar coste/retardo de servicios IoE; dominio ajeno al testing de mutación y a la seguridad de APIs.

> a new rapid mutation operator is incorporated with multi-objective differential evolution (MODE) to overcome the stagnation of the local optimum".

**Hybrid Scheduling Strategy in Cloud Computing based on Optimization Algorithms**  
`ID 23` · 2021 · (no venue field) · 10.1109/ICCMST54943.2021.00022

*Reason.* Cloud task scheduling with genetic algorithms; the term "mutation operator" is the evolutionary-computation sense, not mutation testing, and there is no API or service testing/security content.

> effective scheduling algorithms remain a key issue in cloud computing"; "choose solutions with improved fitness factors, crossover, and mutation operators

**Mutative BFO-Based Scheduling Algorithm for Cloud Environment**  
`ID 24` · 2021 · Lecture Notes in Networks and Systems · 10.1007/978-981-33-6546-9_56

*Reason.* Job scheduling by bacterial foraging optimization; mutation is a metaheuristic operator, unrelated to testing or API/service security.

> a job scheduling algorithm for mapping resources to the job is proposed by applying the mutation operator to Bacterial Foraging Optimization (BFO) algorithm

**Cost-Driven Scheduling for Deadline-Based Workflow Across Multiple Clouds**  
`ID 27` · 2018 · IEEE Transactions on Network and Service Management · 10.1109/TNSM.2018.2872066

*Reason.* Workflow scheduling and cost optimization across clouds; the mutation operator is part of a genetic/PSO metaheuristic, with no testing or API security content.

> proposes a scheduling strategy for a deadline-constrained scientific workflow across multiple clouds"; "randomly single point mutation operator of the genetic algorithm

**A new multi-objective evolutionary algorithm for inter-cloud service composition**  
`ID 28` · 2018 · KSII Transactions on Internet and Information Systems · 10.3837/tiis.2018.01.001

*Reason.* QoS-driven service composition solved by a multi-objective evolutionary algorithm; adaptive mutation operator is metaheuristic, and the paper addresses neither testing nor service security.

> A new hybrid multi-objective evolutionary algorithm ... LS-NSGA-II-DE"; "the differential evolution (DE) algorithm uses the adaptive mutation operator and crossover operator

**RNA-TVcurve: A Web server for RNA secondary structure comparison based on a multi-scale similarity of its triple vector curve representation**  
`ID 29` · 2017 · BMC Bioinformatics · 10.1186/s12859-017-1481-7

*Reason.* Bioinformatics tool for RNA structure comparison; "mutation" is biological point mutation and "web server" is only the delivery form, so it is a completely different area.

> An alignment-free RNA comparison algorithm was proposed"; "detection of single-point mutation based on secondary structure

**Evolutionary web service composition: A graph-based memetic algorithm**  
`ID 31` · 2016 · (no venue field) · 10.1109/CEC.2016.7743796

*Reason.* QoS-aware web service composition optimization by a memetic algorithm; mutation is an evolutionary operator and the work involves no testing or security evaluation.

> we propose a novel Graph-Based Memetic Algorithm (GBMA) for solving the QoS-aware WSC problems"; "overcome the drawbacks of the mutation operator in GraphEvol

**An improved genetic algorithm of web services composition with QOS**  
`ID 35` · 2012 · Advanced Materials Research · 10.4028/www.scientific.net/AMR.532-533.1836

*Reason.* Genetic-algorithm optimization of QoS-aware web service composition; the mutation operator is a genetic operator and no testing or security aspect is addressed.

> A web service composition method based on the adaptive genetic operator was proposed"; "Adaptive crossover and mutation operator were designed according to the individual adaptability

**A genetic: Algorithm approach to cost-based multi-QoS job scheduling in cloud computing environment**  
`ID 39` · 2011 · (no venue field) · 10.1145/1980022.1980111

*Reason.* Cloud job scheduling by genetic algorithm; swap/insertion mutation operators are metaheuristic, unrelated to testing or API security.

> a genetic algorithm approach to cost based multi QoS job scheduling has been proposed"; "mutation operators, swap and insertion mutation are used to produce a better schedule

### RQ3 (12 studies)

**An Adversarial Machine Learning Approach on Securing Large Language Model with Vigil, an Open-Source Initiative**  
`ID 45` · 2024 · Procedia Computer Science · 10.1016/j.procs.2024.09.486

*Reason.* Subject matter is LLM prompt-injection security, not API/web service security nor mutation testing; the REST API is only the tool's delivery mechanism.

> Vigil is an open-source LLM prompt security scanner, that is accessible as a Python library and REST API"; keywords "Prompt Injection; Adversarial Machine Learning; Natural Language Processing

**Fast Blocking of Malicious Traffic by Excluding Benign Flow Monitoring in IDS/SDN Cooperative Firewall Systems**  
`ID 58` · 2022 · ACM International Conference Proceeding Series · 10.1145/3570748.3570757

*Reason.* Purely network-level intrusion detection and firewall traffic blocking; no API, web service, or mutation testing content.

> an SDN switch relays traffic between external and internal networks and mirrors the traffic to an IDS host"; keywords "Firewall; Ids; Networks; Sdn

**Data Mining Model Framework for GTD (Global Terrorism Database)**  
`ID 60` · 2022 · (no venue field) · 10.1109/ICCR56254.2022.9995939

*Reason.* Terrorism data mining and visualization, an entirely unrelated domain.

> The Data Science Model is based on the Global Terrorism Database (GTD) which contains the records off terrorist attacks since 1970"; keywords "Counter-terrorism; Data Mining

**Automation of active reconnaissance phase: An automated API-based port and vulnerability scanner**  
`ID 62` · 2021 · (no venue field) · 10.1145/3487351.3492720

*Reason.* Nmap-based network reconnaissance (IP/port scanning, service enumeration); the API is the implementation vehicle of the scanner, not the security target, so it lies outside API/web service testing and mutation testing.

> an automated API-based IP and port scanner, service-version enumerator, and vulnerability detection system. This scheme is based on the Network Mapper (Nmap)"; keywords "Nmap; Port Scanner; Cyber Reconnaissance

**Preventing Distributed Denial of Service Attacks in Software Defined Mesh Networks**  
`ID 63` · 2021 · (no venue field) · 10.1109/CONIT51480.2021.9498378

*Reason.* Network-layer DDoS detection and mitigation in SDN mesh topologies; the REST API is only the actuator used to push flow policies, not the object of study.

> using SDN capabilities and sFlow-RT application, Distributed Denial of Service (DDoS) attacks is detected and consequently mitigated by using REST API to implement Policy Based Flow Management (PBFM)"; keywords: Mesh networking, Flow tables, Backbone network

**SDN Enabled QoE and Security Framework for Multimedia Applications in 5G Networks**  
`ID 64` · 2021 · ACM Transactions on Multimedia Computing, Communications and Applications · 10.1145/3377390

*Reason.* 5G/SDN-NFV multimedia framework with a lightweight cipher and handover authentication; the RESTful API is a deployment interface, and the work belongs to network/cryptography research, not API or web-service testing/security.

> we propose an SDN/NFV ... framework called STREK"; "a lightweight adaptable hybrid cipher scheme called TREK, and an open RESTful API for applications to deploy custom policies"; keywords: 5G, Network slicing, NFV, Lightweight cryptography

**IBM PAIRS: Scalable big geospatial-temporal data and analytics as-a-service**  
`ID 66` · 2021 · (no venue field) · 10.1007/978-3-030-55462-0_1

*Reason.* Geospatial-temporal big-data platform and analytics-as-a-service; no API security, no service testing, no mutation testing.

> The rapid growth of geospatial-temporal data from sources like satellites, drones, weather modeling, IoT sensors"; "a new paradigm for platforms and services is required" (scalability, harmonization, pixel-level search)

**SADM-SDNC: security anomaly detection and mitigation in software-defined networking using C-support vector classification**  
`ID 68` · 2021 · Computing · 10.1007/s00607-020-00866-x

*Reason.* Machine-learning anomaly detection over NetFlow data in SDN; the REST API appears only as the mitigation-enforcement mechanism, so the study sits in network security, not API security or mutation testing.

> a novel multi-stage modular approach is proposed for detecting and mitigating security anomalies in SDN environment (SADM-SDNC)"; "uses NetFlow protocol for gathering information"; "thanks to utilizing REST API and Static Entry Pusher

**A NEW CAREER PATH PROFILING SYSTEM USING DATA FUSION AND ESCO SERVICES APO**  
`ID 70` · 2021 · eLearning and Software for Education Conference · 10.12753/2066-026X-21-107

*Reason.* Career-recommendation and user-profiling system for education; the ESCO REST API is merely a data source, and there is no testing or security contribution.

> a new system for career recommendations based on advanced analytics of users' profile ... the inference mechanism built in the European qualifications ontology ESCO"; venue: eLearning and Software for Education Conference

**A Software Service Supporting Software Quality Forecasting**  
`ID 72` · 2019 · (no venue field) · 10.1109/QRS-C.2019.00037

*Reason.* Forecasting service for software-quality metrics (ARIMA/ETS) that merely exposes a REST API; no security, no API testing, no mutation testing.

> we have developed a modular and flexible forecasting service ... for creating and exploiting forecasting models based on methods like ARIMA or ETS"; "exposes its functionalities through a REST API

**Facebook Inspector (FbI): Towards automatic real-time detection of malicious content on Facebook**  
`ID 77` · 2017 · Social Network Analysis and Mining · 10.1007/s13278-017-0434-5

*Reason.* Machine-learning detection of malicious posts in an online social network; the REST API only packages the browser plug-in, so the topic lies outside API/service testing and security.

> we collect and characterize a dataset of 4.4 million public posts generated on Facebook"; "we implement Facebook Inspector, a REST API-based browser plug-in"; keywords: Malicious content; Social networking (online)

**Towards automatic real time identification of malicious posts on Facebook**  
`ID 79` · 2015 · (no venue field) · 10.1109/PST.2015.7232958

*Reason.* Machine-learning identification of malicious social-network posts; no API or web-service security, no mutation testing.

> we characterized a dataset of 4.4 million public posts generated on Facebook ... and identified 11,217 malicious posts containing URLs"; keywords: Online social networks (OSNs); Textual content

### RQ4 (3 studies)

**Design and Implementation of a forensic framework for Cloud in OpenStack cloud platform**  
`ID 82` · 2014 · (no venue field) · 10.1109/ICACCI.2014.6968451

*Reason.* Digital/cloud forensics (memory snapshots, disk images, packet captures) in OpenStack; the cloud API is only a channel through which user actions travel, not a testing or security-evaluation target.

> a forensic framework has been developed to do cloud forensics in OpenStack for infrastructure as a service model using the existing forensic tools"; keywords: Cloud forensics; Digital forensics; Computer forensics

**Machine learning-based intelligent security framework for secure cloud key management**  
`ID 112` · 2024 · Cluster Computing · 10.1007/s10586-024-04288-8

*Reason.* Cryptographic key management for cloud environments; security, but not of APIs or web services, and no mutation testing.

> Title "Machine learning-based intelligent security framework for secure cloud key management" (Cluster Computing, 2024); no abstract or keywords, but the title situates the topic squarely in cloud key management.

**SUACC-IoT: secure unified authentication and access control system based on capability for IoT**  
`ID 135` · 2022 · Cluster Computing · 10.1007/s10586-022-03733-w

*Reason.* Borderline but off-scope: the object of study is a capability-based authentication and access control protocol for IoT devices, not testing or security evaluation of APIs, web services, or mutation testing; the parent should re-check if the paper turns out to target RESTful service invocation.

> Title: "secure unified authentication and access control system based on capability for IoT"; venue Cluster Computing

### RQ5 (18 studies)

**A Modular REST-Based Framework for Human-in-the-Loop Robot-Assisted personalized Rehabilitation in Neurodevelopmental Disorders**  
`ID 86` · 2025 · CEUR Workshop Proceedings · (no DOI)

*Reason.* Assistive-robotics rehabilitation platform in which REST is only the implementation interface, the exact kind of unrelated domain the exclusion criteria name.

> Socially Assistive Robots (SARs) are increasingly used in therapeutic settings"; keywords "human-robot interaction; neurodevelopmental disorders; socially assistive robots

**Automated Network Planner Based on Digital Twin for Wavelength Division Multiplexing Network**  
`ID 87` · 2025 · Proceedings of the National Conference on Communications, NCC · 10.1109/NCC63735.2025.10983014

*Reason.* Optical-network planning, an area with no relation to API/web-service testing or security or to mutation testing.

> presents a network planning tool based on Digital Twin technology for Dense Wavelength Division Multiplexing (DWDM) networks"; keywords "DWDM; OTN; Transparent optical networks

**Adaptive mMIMO Control in OPEN RAN: A Dynamic xApp Approach for Energy-Efficient Antenna Management**  
`ID 88` · 2025 · (no venue field) · 10.1109/EuCNC/6GSummit63408.2025.11036926

*Reason.* Radio-access-network antenna and energy management, unrelated to API security or mutation testing despite the incidental REST API keyword.

> an xApp-based algorithm that fetches RAN KPIs to adjust mMIMO parameters and enhance energy efficiency"; keywords "mMIMO; Energy Efficiency; xApp OPEN RAN

**Prototyping the Monitoring Applications in Public Buildings using Edge Computing Paradigm**  
`ID 92` · 2024 · International Conference on Human System Interaction, HSI · 10.1109/HSI61632.2024.10613556

*Reason.* IoT building-monitoring prototype where a REST API is merely one implementation component, outside API testing and security.

> a prototype (mockup) of a system for monitoring environmental parameters in residential and public premises"; keywords "edge computing; internet of things; sensors; single board computers

**Technical Report: Define a customized course and import it into Moodle without changes to the configuration of the Moodle system**  
`ID 94` · 2023 · (no venue field) · 10.1145/3593663.3593668

*Reason.* Learning-management-system course authoring; the Moodle REST-API is mentioned only as a rejected alternative, so the study belongs to an unrelated area.

> defining a customized course in Moodle, a popular learning management system ... the structure of Moodle backup zip (MBZ) files

**Conversation Disentanglement As-a-Service**  
`ID 95` · 2023 · (no venue field) · 10.1109/ICPC58990.2023.00018

*Reason.* Program-comprehension and NLP tooling packaged as a RESTful micro-service, with no API security or testing contribution.

> Associating messages to conversations is called conversation disentanglement, a useful and necessary pre-processing step to analyze datasets of instant messages"; keywords "conversation disentanglement; instant messaging

**Conceptualizing Node.js Projects: A Graph-Oriented Technology-Specific Modeling Method**  
`ID 96` · 2023 · Lecture Notes in Information Systems and Organisation · 10.1007/978-3-031-32418-5_4

*Reason.* Domain-specific conceptual modeling for dependency and project management, unrelated to API security or mutation testing.

> a modeling method for managing Node.js projects dependencies by adding a semantic analysis layer ... knowledge-driven project management approach"; keywords "ADOxx; Dependency management; RDF

**Teaching Guide for Beginnings in DevOps and Continuous Delivery in AWS Focused on the Society 5.0 Skillset**  
`ID 97` · 2022 · Revista Iberoamericana de Tecnologias del Aprendizaje · 10.1109/RITA.2022.3217172

*Reason.* Software-engineering education and DevOps pedagogy; the REST API is only the course exercise artifact.

> presents a didactic guide that allows the adoption of good development practices, strengthening soft and technical skills ... within systems engineering programs"; keywords "teaching guide; society 50; CI; CD

**Toolchains for Interoperable BIM Workflows in a Web-Based Integration Platform**  
`ID 98` · 2022 · Applied Sciences (Switzerland) · 10.3390/app12125959

*Reason.* Building-information-modeling workflow integration for the construction industry, an unrelated application domain.

> The construction industry is characterized by the diversity of its processes ... collaborative BIM workflows"; keywords "BIM; information container; openCDE

**The Design of the Spacecraft Test System 4000 Based on Microservices Running in Cloud Environment**  
`ID 99` · 2022 · Proceedings of the International Astronautical Congress, IAC · (no DOI)

*Reason.* Aerospace ground-support test equipment architecture; the word test refers to spacecraft hardware validation, not software API testing.

> the electrical ground support equipment (EGSE) must ... exhibit a high degree of extensibility"; keywords "spacecraft test system; cloud computing; Aerospace industry

**Incorporating Personality Traits in User Modeling for EUD**  
`ID 100` · 2022 · CEUR Workshop Proceedings · (no DOI)

*Reason.* HCI and user-modeling psychology in end-user development; the REST API is only the query interface to the services.

> Personality traits such as Need for Cognition, Locus of Control, Mindset and Self-efficacy could impact the perception, acceptance and appreciation of recommendations"; keywords "psychological traits; rule recommendation

**Remote dynamic reconfiguration of a multi-FPGA system FiC (flow-in-cloud)**  
`ID 104` · 2021 · IEICE Transactions on Information and Systems · 10.1587/transinf.2020EDP7165

*Reason.* Reconfigurable-hardware / FPGA cluster management paper; the REST API is only the control interface of the prototype, and the domain is unrelated to API testing or security.

> a bare-metal multi-FPGA system called FiC (Flow-in-Cloud)... applied partial reconfiguration (PR) FPGA design flow"; keywords "Field programmable gate arrays (FPGA); Interconnection networks; Bitstream compression".

**Enabling complexity management through merging business process modeling with MBSE**  
`ID 105` · 2019 · Procedia CIRP · 10.1016/j.procir.2019.04.267

*Reason.* Model-based systems engineering for product development processes; no APIs, no web services, no mutation testing.

> This paper presents an approach for merging MBSE with business processes"; keywords "Complexity management; Integral product architecture; Model based systems engineering; Product development process".

**Hands-on Azure Boards: Configuring and Customizing Process Workflows in Azure DevOps Services**  
`ID 106` · 2019 · (no venue field) · 10.1007/9781484250464

*Reason.* Practitioner book on agile work-item management in Azure DevOps; agile project management is one of the domains explicitly outside the bibliometric scope.

> keywords "Agile; Azure; Azure Boards; Kanban; Scrum"; "how to effectively use Azure Boards to plan and execute work" — REST API mentioned only as an administration channel.

**Architecting a Software-Defined Storage Platform for Cloud Storage Service**  
`ID 107` · 2015 · (no venue field) · 10.1109/SCC.2015.59

*Reason.* Storage-system architecture paper; RESTful APIs appear only as a business-extension interface of the platform, not as an object of testing or security analysis.

> the architecture of a new SDS platform called Federator is proposed"; "3. Restful APIs for new business extension"; keywords "Digital storage; Software-Defined storage; Predictive analytics".

**FTS3 - A file transfer service for Grids, HPCs and Clouds**  
`ID 108` · 2015 · Proceedings of Science · (no DOI)

*Reason.* Grid data-transfer service and web front end; file transfer infrastructure is a domain unrelated to API/web-service testing or security.

> FTS3, the service responsible for globally distributing the majority of the LHC data across the WLCG infrastructure"; the only relevant mention is "accessed through our standards-compliant REST API" and a "zero configuration" deployment claim.

**FTS3 / WebFTS - A Powerful File Transfer Service for Scientific Communities**  
`ID 109` · 2015 · Procedia Computer Science · 10.1016/j.procs.2015.11.076

*Reason.* Same file-transfer service as the previous record (near-duplicate content, different venue); out-of-domain and also duplicated.

> In this article we describe this intuitive new interface, \"WebFTS\", which allows users to easily schedule and manage large data transfers right from the browser"; keywords "Data storage; File transfer; FTS3; WebFTS".

**OM2M: Extensible ETSI-compliant M2M service platform with self-configuration capability**  
`ID 111` · 2014 · Procedia Computer Science · 10.1016/j.procs.2014.05.536

*Reason.* IoT/M2M middleware architecture paper; the RESTful API is an interoperability feature and the self-configuration discussed is autonomic device management, not security or testing.

> we propose the open source OM2 M project, an autonomic ETSI-compliant M2 M service platform... OM2 M provides a RESTful API to enhance interoperability"; keywords "ETSI M2 M; Internet of Things; Autonomic Computing; Self-configuration".

## Proposed exclusions that were rescued

These studies were flagged in the first pass and are retained.

**Sifu Reloaded: An Open-Source Gamified Web-Based CyberSecurity Awareness Platform**  
`ID 49` · 2023 · OpenAccess Series in Informatics

*Retained because.* The paper's object is software vulnerabilities and secure coding: the Sifu platform automatically assesses submitted code for compliance with secure-coding guidelines over deliberately vulnerable challenge artifacts, i.e. automated security evaluation of code against seeded vulnerabilities, which falls inside the software-security neighborhood the wide bibliometric scope admits and matches its RQ3 assignment (factors contributing to finding vulnerabilities). The reviewer is right that the REST API is only the platform's own client/server architecture and that there is no mutation testing, so it belongs to the bibliometric periphery, not the substantive core — but that makes it adjacent, not an unrelated domain such as cloud scheduling or image encryption.

**Blockchain-Based Services Implemented in a Microservices Architecture Using a Trusted Platform Module Applied to Electric Vehicle Charging Stations**  
`ID 50` · 2023 · Energies

*Retained because.* El aporte de seguridad del artículo recae sobre la propia superficie REST del microservicio, no sobre el dominio energético: propone un mecanismo de autenticación por tokens (Cognito, doble factor) para impedir el acceso no autorizado a la API que expone el TPM virtualizado, más atestación y sellado para garantizar la integridad del servicio contenerizado; las palabras clave indexadas lo confirman (Web Services, Authentication, Microservice Architecture, Containers). Eso es seguridad de servicios web y de arquitecturas de microservicios —una estrategia de mitigación de control de acceso a API, encajable en RQ4/RQ5 y en categorías tipo API2/API8—, dominio adyacente que el alcance bibliométrico admite de forma explícita; la estación de carga de vehículos eléctricos es solo el caso de aplicación (salvedad honesta: no hay testing de mutación ni evaluación de seguridad, solo una prueba de concepto, por lo que su valor es bibliométrico y no sustantivo).

**Enhancing blockchain security through natural language processing and real-time monitoring**  
`ID 52` · 2023 · International Journal of Parallel, Emergent and Distributed Systems

*Retained because.* Under the broad bibliometric scope the study qualifies as adjacent service-security work: it empirically implements and tests a runtime security monitoring service for a deployed service-oriented platform, exposed through a REST API, whose detection targets include DDoS and misconfigured Docker containers — the same vulnerability classes the thesis treats as OWASP API4 and API8, matching its RQ3/RQ5 remit. It is software/service security rather than a foreign domain (no cloud scheduling, encryption or data mining here), so it should be retained for bibliometric purposes only, with the caveat that it involves no mutation testing and does not test the API itself.

**An Environment-Specific Prioritization Model for Information-Security Vulnerabilities Based on Risk Factor Analysis**  
`ID 59` · 2022 · Electronics (Switzerland)

*Retained because.* It is an empirically validated software-security study on detecting and prioritizing vulnerabilities in internet-exposed services, correctly assigned to RQ3 (factors contributing to finding vulnerabilities), so it falls inside the broad bibliometric scope rather than in an unrelated domain like scheduling or encryption. Its core result — that CVSS base scores are insufficient without environment-specific risk factors — is the direct evidentiary basis for the thesis's CVSS-aligned severity field and the Weighted Mutation Score; the Shodan REST API is indeed incidental and is not the ground for the rescue.

**Trustworthy Data Analysis and Sensor Data Protection in Cyber-Physical Systems**  
`ID 67` · 2021 · (no venue field)

*Retained because.* The proposed artifact is a secure data container exposed through a RESTful API serving signed/encrypted JSON, and its security contribution is enforcement of fine-grained role-based and attribute-based access control plus data confidentiality/integrity on that interface — the same authorization and data-exposure concern space as REST API security, which the bibliometric scope admits as adjacent web-service security work rather than an unrelated domain. The rescue holds only for the broad bibliometric scope and RQ3 context: the paper does no mutation testing and no API testing, so it must not be counted as an API-testing or mutation-testing primary study.

**TRACER: A platform for securing legacy code**  
`ID 81` · 2014 · Lecture Notes in Computer Science

*Retained because.* TRACER sits squarely in software security vulnerability detection — it aggregates static-analysis detectors (FindBugs, Frama-C) to track security defects across a project's evolution, and it exposes its analysis results through a REST API — so it is adjacent-domain security-testing work, not a foreign field like cloud scheduling or image encryption; under the declared bibliometric scope (which "counts every primary study against each research question for which it supplies contextual evidence, including studies not centrally focused on RESTful API security mutation testing") it legitimately supplies contextual evidence for its assigned RQ3 on vulnerability-detection factors and detector-output heterogeneity. Caveat in fairness: at two pages (218-219) it is an extended abstract with only a demonstration of two plug-ins, so "theoretical/tool sketch without empirical validation" would be a far stronger exclusion ground than the topical one proposed — but that ground was not the one invoked.

**A Web-Based Monitoring System of Network Security Functions in Blockchain-Based Cloud Security Systems**  
`ID 101` · 2022 · International Conference on Information Networking

*Retained because.* El objeto del trabajo es la interfaz misma: implementa la Monitoring Interface del marco I2NSF del IETF —interfaces estandarizadas y modelos de datos para configurar y monitorizar funciones de seguridad— mediante una REST API sobre el SDK de Hyperledger, y su aportación de seguridad es la integridad no manipulable de los datos que esa API entrega, es decir, una propiedad de seguridad que recae sobre el servicio web, no solo sobre la red (de ahí su asignación coherente a RQ5, configuración segura de funciones de seguridad; los index keywords de Scopus incluyen "Application programming interfaces (API)"). No es un dominio ajeno como planificación cloud o cifrado de imágenes, así que bajo el alcance bibliométrico amplio —que admite explícitamente seguridad de servicios web en general— es INCLUDE, aunque conviene registrarlo como adyacente: no contiene testing de mutación ni evaluación de vulnerabilidades de la API, y no debe contarse como estudio sustantivo.

**Permissioned Blockchain Reinforced API Platform for Data Management in IoT-based Sensor Networks**  
`ID 102` · 2021 · Proceedings - IEEE Global Communications Conference, GLOBECOM

*Retained because.* The contributed artifact is itself a REST API platform whose permissioned-blockchain plus smart-contract layer is the access-control and data-integrity mechanism sitting behind the endpoint, and it is empirically benchmarked (latency, throughput) against a commercial REST API service, so the study lands in security architecture of a RESTful/IoT API rather than in an unrelated field, an adjacency the bibliometric scope admits and that the thesis's own extraction schema anticipates by listing "IoT API" as a valid target system. The honest caveat is that no API-level security property is ever tested or measured, so it holds only as broad-scope contextual evidence for RQ5 and must never be counted in the substantive corpus.

**R4R: Template-based REST API Framework for RDF Knowledge Graphs**  
`ID 103` · 2021 · CEUR Workshop Proceedings

*Retained because.* R4R sits squarely inside the RESTful API / web services domain the bibliometric scope admits: it builds and publishes REST APIs over SPARQL endpoints, and its API surface is defined entirely by declarative configuration files and query directories, with web authentication as an explicit feature — exactly the configuration-and-auth surface that RQ5 (security misconfiguration, OWASP API8/API9) studies, which is why it carries that RQ assignment. It is not a testing or security paper substantively, so it does not belong to the narrow scope, but it is not a foreign domain either (unlike cloud scheduling or image encryption), and excluding it as "not directly related to RESTful API security or mutation testing" would misapply a criterion aimed at unrelated fields to a paper whose entire subject is REST API construction and exposure.

