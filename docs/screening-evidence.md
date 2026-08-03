---
title: Screening decisions and their evidence
author: Carlos A. Delgado S.
version: 1.0
status: final
tags: [slr, prisma, screening, corpus]
---

# Screening decisions

Studies were judged against the inclusion and exclusion criteria of the review, in particular the two exclusion clauses that read *Publications not directly related to RESTful API security or mutation testing* and *Articles focusing on non-RESTful API security or unrelated mutation testing domains*. The scope of the review admits adjacent work on web services, fault injection and stateful fuzzing, so a study is excluded only when it belongs to a different field altogether.

- Studies judged: **160**
- Included: **114**
- Excluded: **46**

Each exclusion carries its reason and a verbatim fragment of the source record behind it, so a decision can be checked study by study rather than accepted wholesale. The included studies are listed with their characteristics in `../data/corpus.csv`.

## Excluded studies

### RQ1 (4 studies)

**Resource optimization of container orchestration: a case study in multi-cloud microservices-based applications**  
2018 · Journal of Supercomputing · 10.1007/s11227-018-2345-2

*Reason.* Optimización de despliegue de contenedores con NSGA-II; los operadores de mutación son genéticos, sin relación con testing ni seguridad de APIs.

> optimize the deployment of microservices-based applications using containers ... NSGA-II with a two-point crossover operator and three mutation operators".

**Many-Objective Optimization-Based Task Scheduling in Hybrid Cloud Environments**  
2023 · CMES - Computer Modeling in Engineering and Sciences · 10.32604/cmes.2023.026671

*Reason.* Planificación de tareas en nube con algoritmos evolutivos; el "mutation operator" es de computación evolutiva, no testing de mutación ni seguridad de APIs.

> a many-objective hybrid cloud task scheduling optimization model (HCTSO)... a dynamic range mutation operator are designed to extend the search range".

**Preserving privacy while revealing thumbnail for content-based encrypted image retrieval in the cloud**  
2022 · Information Sciences · 10.1016/j.ins.2022.05.008

*Reason.* Cifrado y recuperación de imágenes con algoritmos genéticos; dominio ajeno al testing/seguridad de APIs y servicios web.

> a thumbnail preserving encryption (TPE) based on genetic algorithm ... through crossover and mutation operators of the genetic algorithm".

**Cloud computing resource scheduling and leasing algorithm based on extreme price filter**  
2017 · International Journal of Reasoning-based Intelligent Systems · 10.1504/ijris.2017.090036

*Reason.* Planificación y arriendo de recursos en la nube por precio; mutación no uniforme de un algoritmo genético, dominio no relacionado.

> cloud computing virtual resource leasing algorithm considering about extreme price filtering ... non-uniform mutation operator has been used to make local operating adjusting".

### RQ2 (11 studies)

**A genetic: Algorithm approach to cost-based multi-QoS job scheduling in cloud computing environment**  
2011 · International Conference and Workshop on Emerging Trends in Technology 2011, ICWET 2011 · 10.1145/1980022.1980111

*Reason.* Cloud job scheduling by genetic algorithm; swap/insertion mutation operators are metaheuristic, unrelated to testing or API security.

> a genetic algorithm approach to cost based multi QoS job scheduling has been proposed"; "mutation operators, swap and insertion mutation are used to produce a better schedule

**Hybrid Scheduling Strategy in Cloud Computing based on Optimization Algorithms**  
2021 · 2nd International Conference on Computational Methods in Science and Technology, ICCMST 2021 · 10.1109/iccmst54943.2021.00022

*Reason.* Cloud task scheduling with genetic algorithms; the term "mutation operator" is the evolutionary-computation sense, not mutation testing, and there is no API or service testing/security content.

> effective scheduling algorithms remain a key issue in cloud computing"; "choose solutions with improved fitness factors, crossover, and mutation operators

**A new multi-objective evolutionary algorithm for inter-cloud service composition**  
2018 · KSII Transactions on Internet and Information Systems · 10.3837/tiis.2018.01.001

*Reason.* QoS-driven service composition solved by a multi-objective evolutionary algorithm; adaptive mutation operator is metaheuristic, and the paper addresses neither testing nor service security.

> A new hybrid multi-objective evolutionary algorithm ... LS-NSGA-II-DE"; "the differential evolution (DE) algorithm uses the adaptive mutation operator and crossover operator

**Evolutionary web service composition: A graph-based memetic algorithm**  
2016 · 2016 IEEE Congress on Evolutionary Computation, CEC 2016 · 10.1109/cec.2016.7743796

*Reason.* QoS-aware web service composition optimization by a memetic algorithm; mutation is an evolutionary operator and the work involves no testing or security evaluation.

> we propose a novel Graph-Based Memetic Algorithm (GBMA) for solving the QoS-aware WSC problems"; "overcome the drawbacks of the mutation operator in GraphEvol

**A hybrid genetic-based task scheduling algorithm for cost-efficient workflow execution in heterogeneous cloud computing environment**  
2024 · Cluster Computing · 10.1007/s10586-024-04468-6

*Reason.* Planificación de workflows en la nube con algoritmo genético híbrido; sin testing ni seguridad de APIs o servicios web.

> a hybrid genetic algorithm (HGA) is presented for reliable and cost-efficient task scheduling ... new crossover and mutation operators for global search".

**Mutative BFO-Based Scheduling Algorithm for Cloud Environment**  
2021 · Lecture Notes in Networks and Systems · 10.1007/978-981-33-6546-9_56

*Reason.* Job scheduling by bacterial foraging optimization; mutation is a metaheuristic operator, unrelated to testing or API/service security.

> a job scheduling algorithm for mapping resources to the job is proposed by applying the mutation operator to Bacterial Foraging Optimization (BFO) algorithm

**A Novel Multi-Objective Optimization Based Evolutionary Algorithm for Optimize the Services of Internet of Everything**  
2022 · IEEE Access · 10.1109/access.2022.3209389

*Reason.* Algoritmo evolutivo multiobjetivo para optimizar coste/retardo de servicios IoE; dominio ajeno al testing de mutación y a la seguridad de APIs.

> a new rapid mutation operator is incorporated with multi-objective differential evolution (MODE) to overcome the stagnation of the local optimum".

**Cost-Driven Scheduling for Deadline-Based Workflow Across Multiple Clouds**  
2018 · IEEE Transactions on Network and Service Management · 10.1109/tnsm.2018.2872066

*Reason.* Workflow scheduling and cost optimization across clouds; the mutation operator is part of a genetic/PSO metaheuristic, with no testing or API security content.

> proposes a scheduling strategy for a deadline-constrained scientific workflow across multiple clouds"; "randomly single point mutation operator of the genetic algorithm

**RNA-TVcurve: A Web server for RNA secondary structure comparison based on a multi-scale similarity of its triple vector curve representation**  
2017 · BMC Bioinformatics · 10.1186/s12859-017-1481-7

*Reason.* Bioinformatics tool for RNA structure comparison; "mutation" is biological point mutation and "web server" is only the delivery form, so it is a completely different area.

> An alignment-free RNA comparison algorithm was proposed"; "detection of single-point mutation based on secondary structure

**An improved genetic algorithm of web services composition with QOS**  
2012 · Advanced Materials Research · 10.4028/www.scientific.net/amr.532-533.1836

*Reason.* Genetic-algorithm optimization of QoS-aware web service composition; the mutation operator is a genetic operator and no testing or security aspect is addressed.

> A web service composition method based on the adaptive genetic operator was proposed"; "Adaptive crossover and mutation operator were designed according to the individual adaptability

**NSGA-II-AMO: A Faster Genetic Algorithm for QWSCP**  
2023 · Studies in Computational Intelligence · 10.1007/978-3-031-19604-1_15

*Reason.* Optimización evolutiva de la composición de servicios web por QoS: ni testing ni seguridad, y el operador de mutación es genético.

> QoS-driven web service composition problem (QWSCP) ... uses an adaptive mutation operator to complete the mutation process when generating children in the NSGA-II algorithm".

### RQ3 (12 studies)

**Fast Blocking of Malicious Traffic by Excluding Benign Flow Monitoring in IDS/SDN Cooperative Firewall Systems**  
2022 · ACM International Conference Proceeding Series · 10.1145/3570748.3570757

*Reason.* Purely network-level intrusion detection and firewall traffic blocking; no API, web service, or mutation testing content.

> an SDN switch relays traffic between external and internal networks and mirrors the traffic to an IDS host"; keywords "Firewall; Ids; Networks; Sdn

**An Adversarial Machine Learning Approach on Securing Large Language Model with Vigil, an Open-Source Initiative**  
2024 · Procedia Computer Science · 10.1016/j.procs.2024.09.486

*Reason.* Subject matter is LLM prompt-injection security, not API/web service security nor mutation testing; the REST API is only the tool's delivery mechanism.

> Vigil is an open-source LLM prompt security scanner, that is accessible as a Python library and REST API"; keywords "Prompt Injection; Adversarial Machine Learning; Natural Language Processing

**Automation of active reconnaissance phase: An automated API-based port and vulnerability scanner**  
2021 · 13th IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining, ASONAM 2021 · 10.1145/3487351.3492720

*Reason.* Nmap-based network reconnaissance (IP/port scanning, service enumeration); the API is the implementation vehicle of the scanner, not the security target, so it lies outside API/web service testing and mutation testing.

> an automated API-based IP and port scanner, service-version enumerator, and vulnerability detection system. This scheme is based on the Network Mapper (Nmap)"; keywords "Nmap; Port Scanner; Cyber Reconnaissance

**A Software Service Supporting Software Quality Forecasting**  
2019 · 19th IEEE International Conference on Software Quality, Reliability and Security Companion, QRS-C 2019 · 10.1109/qrs-c.2019.00037

*Reason.* Forecasting service for software-quality metrics (ARIMA/ETS) that merely exposes a REST API; no security, no API testing, no mutation testing.

> we have developed a modular and flexible forecasting service ... for creating and exploiting forecasting models based on methods like ARIMA or ETS"; "exposes its functionalities through a REST API

**A NEW CAREER PATH PROFILING SYSTEM USING DATA FUSION AND ESCO SERVICES APO**  
2021 · eLearning and Software for Education Conference · 10.12753/2066-026x-21-107

*Reason.* Career-recommendation and user-profiling system for education; the ESCO REST API is merely a data source, and there is no testing or security contribution.

> a new system for career recommendations based on advanced analytics of users' profile ... the inference mechanism built in the European qualifications ontology ESCO"; venue: eLearning and Software for Education Conference

**Data Mining Model Framework for GTD (Global Terrorism Database)**  
2022 · 2022 International Conference on Cyber Resilience, ICCR 2022 · 10.1109/iccr56254.2022.9995939

*Reason.* Terrorism data mining and visualization, an entirely unrelated domain.

> The Data Science Model is based on the Global Terrorism Database (GTD) which contains the records off terrorist attacks since 1970"; keywords "Counter-terrorism; Data Mining

**Towards automatic real time identification of malicious posts on Facebook**  
2015 · 13th Annual Conference on Privacy, Security and Trust, PST 2015 · 10.1109/pst.2015.7232958

*Reason.* Machine-learning identification of malicious social-network posts; no API or web-service security, no mutation testing.

> we characterized a dataset of 4.4 million public posts generated on Facebook ... and identified 11,217 malicious posts containing URLs"; keywords: Online social networks (OSNs); Textual content

**Facebook Inspector (FbI): Towards automatic real-time detection of malicious content on Facebook**  
2017 · Social Network Analysis and Mining · 10.1007/s13278-017-0434-5

*Reason.* Machine-learning detection of malicious posts in an online social network; the REST API only packages the browser plug-in, so the topic lies outside API/service testing and security.

> we collect and characterize a dataset of 4.4 million public posts generated on Facebook"; "we implement Facebook Inspector, a REST API-based browser plug-in"; keywords: Malicious content; Social networking (online)

**SDN Enabled QoE and Security Framework for Multimedia Applications in 5G Networks**  
2021 · ACM Transactions on Multimedia Computing, Communications and Applications · 10.1145/3377390

*Reason.* 5G/SDN-NFV multimedia framework with a lightweight cipher and handover authentication; the RESTful API is a deployment interface, and the work belongs to network/cryptography research, not API or web-service testing/security.

> we propose an SDN/NFV ... framework called STREK"; "a lightweight adaptable hybrid cipher scheme called TREK, and an open RESTful API for applications to deploy custom policies"; keywords: 5G, Network slicing, NFV, Lightweight cryptography

**IBM PAIRS: Scalable big geospatial-temporal data and analytics as-a-service**  
2021 · (no venue field) · 10.1007/978-3-030-55462-0_1

*Reason.* Geospatial-temporal big-data platform and analytics-as-a-service; no API security, no service testing, no mutation testing.

> The rapid growth of geospatial-temporal data from sources like satellites, drones, weather modeling, IoT sensors"; "a new paradigm for platforms and services is required" (scalability, harmonization, pixel-level search)

**Preventing Distributed Denial of Service Attacks in Software Defined Mesh Networks**  
2021 · 2021 International Conference on Intelligent Technologies, CONIT 2021 · 10.1109/conit51480.2021.9498378

*Reason.* Network-layer DDoS detection and mitigation in SDN mesh topologies; the REST API is only the actuator used to push flow policies, not the object of study.

> using SDN capabilities and sFlow-RT application, Distributed Denial of Service (DDoS) attacks is detected and consequently mitigated by using REST API to implement Policy Based Flow Management (PBFM)"; keywords: Mesh networking, Flow tables, Backbone network

**SADM-SDNC: security anomaly detection and mitigation in software-defined networking using C-support vector classification**  
2021 · Computing · 10.1007/s00607-020-00866-x

*Reason.* Machine-learning anomaly detection over NetFlow data in SDN; the REST API appears only as the mitigation-enforcement mechanism, so the study sits in network security, not API security or mutation testing.

> a novel multi-stage modular approach is proposed for detecting and mitigating security anomalies in SDN environment (SADM-SDNC)"; "uses NetFlow protocol for gathering information"; "thanks to utilizing REST API and Static Entry Pusher

### RQ4 (1 studies)

**Design and Implementation of a forensic framework for Cloud in OpenStack cloud platform**  
2014 · Proc. Int. Conf. Adv. Comput., Commun. Informatics, ICACCI · 10.1109/icacci.2014.6968451

*Reason.* Digital/cloud forensics (memory snapshots, disk images, packet captures) in OpenStack; the cloud API is only a channel through which user actions travel, not a testing or security-evaluation target.

> a forensic framework has been developed to do cloud forensics in OpenStack for infrastructure as a service model using the existing forensic tools"; keywords: Cloud forensics; Digital forensics; Computer forensics

### RQ5 (18 studies)

**Prototyping the Monitoring Applications in Public Buildings using Edge Computing Paradigm**  
2024 · International Conference on Human System Interaction, HSI · 10.1109/hsi61632.2024.10613556

*Reason.* IoT building-monitoring prototype where a REST API is merely one implementation component, outside API testing and security.

> a prototype (mockup) of a system for monitoring environmental parameters in residential and public premises"; keywords "edge computing; internet of things; sensors; single board computers

**OM2M: Extensible ETSI-compliant M2M service platform with self-configuration capability**  
2014 · Procedia Computer Science · 10.1016/j.procs.2014.05.536

*Reason.* IoT/M2M middleware architecture paper; the RESTful API is an interoperability feature and the self-configuration discussed is autonomic device management, not security or testing.

> we propose the open source OM2 M project, an autonomic ETSI-compliant M2 M service platform... OM2 M provides a RESTful API to enhance interoperability"; keywords "ETSI M2 M; Internet of Things; Autonomic Computing; Self-configuration".

**Technical Report: Define a customized course and import it into Moodle without changes to the configuration of the Moodle system**  
2023 · 5th European Conference on Software Engineering Education, ECSEE 2023 · 10.1145/3593663.3593668

*Reason.* Learning-management-system course authoring; the Moodle REST-API is mentioned only as a rejected alternative, so the study belongs to an unrelated area.

> defining a customized course in Moodle, a popular learning management system ... the structure of Moodle backup zip (MBZ) files

**Incorporating Personality Traits in User Modeling for EUD**  
2022 · CEUR Workshop Proceedings · (no DOI)

*Reason.* HCI and user-modeling psychology in end-user development; the REST API is only the query interface to the services.

> Personality traits such as Need for Cognition, Locus of Control, Mindset and Self-efficacy could impact the perception, acceptance and appreciation of recommendations"; keywords "psychological traits; rule recommendation

**Hands-on Azure Boards: Configuring and Customizing Process Workflows in Azure DevOps Services**  
2019 · Hands-on Azure Boards: Configuring and Customizing Process. Workflows in Azure DevOps Services · 10.1007/9781484250464

*Reason.* Practitioner book on agile work-item management in Azure DevOps; agile project management is one of the domains explicitly outside the bibliometric scope.

> keywords "Agile; Azure; Azure Boards; Kanban; Scrum"; "how to effectively use Azure Boards to plan and execute work" — REST API mentioned only as an administration channel.

**The Design of the Spacecraft Test System 4000 Based on Microservices Running in Cloud Environment**  
2022 · Proceedings of the International Astronautical Congress, IAC · (no DOI)

*Reason.* Aerospace ground-support test equipment architecture; the word test refers to spacecraft hardware validation, not software API testing.

> the electrical ground support equipment (EGSE) must ... exhibit a high degree of extensibility"; keywords "spacecraft test system; cloud computing; Aerospace industry

**Adaptive mMIMO Control in OPEN RAN: A Dynamic xApp Approach for Energy-Efficient Antenna Management**  
2025 · 2025 Joint European Conference on Networks and Communications and 6G Summit, EuCNC/6G Summit 2025 · 10.1109/eucnc/6gsummit63408.2025.11036926

*Reason.* Radio-access-network antenna and energy management, unrelated to API security or mutation testing despite the incidental REST API keyword.

> an xApp-based algorithm that fetches RAN KPIs to adjust mMIMO parameters and enhance energy efficiency"; keywords "mMIMO; Energy Efficiency; xApp OPEN RAN

**A Modular REST-Based Framework for Human-in-the-Loop Robot-Assisted personalized Rehabilitation in Neurodevelopmental Disorders**  
2025 · CEUR Workshop Proceedings · (no DOI)

*Reason.* Assistive-robotics rehabilitation platform in which REST is only the implementation interface, the exact kind of unrelated domain the exclusion criteria name.

> Socially Assistive Robots (SARs) are increasingly used in therapeutic settings"; keywords "human-robot interaction; neurodevelopmental disorders; socially assistive robots

**Toolchains for Interoperable BIM Workflows in a Web-Based Integration Platform**  
2022 · Applied Sciences (Switzerland) · 10.3390/app12125959

*Reason.* Building-information-modeling workflow integration for the construction industry, an unrelated application domain.

> The construction industry is characterized by the diversity of its processes ... collaborative BIM workflows"; keywords "BIM; information container; openCDE

**Remote dynamic reconfiguration of a multi-FPGA system FiC (flow-in-cloud)**  
2021 · IEICE Transactions on Information and Systems · 10.1587/transinf.2020edp7165

*Reason.* Reconfigurable-hardware / FPGA cluster management paper; the REST API is only the control interface of the prototype, and the domain is unrelated to API testing or security.

> a bare-metal multi-FPGA system called FiC (Flow-in-Cloud)... applied partial reconfiguration (PR) FPGA design flow"; keywords "Field programmable gate arrays (FPGA); Interconnection networks; Bitstream compression".

**Architecting a Software-Defined Storage Platform for Cloud Storage Service**  
2015 · IEEE International Conference on Services Computing, SCC 2015 · 10.1109/scc.2015.59

*Reason.* Storage-system architecture paper; RESTful APIs appear only as a business-extension interface of the platform, not as an object of testing or security analysis.

> the architecture of a new SDS platform called Federator is proposed"; "3. Restful APIs for new business extension"; keywords "Digital storage; Software-Defined storage; Predictive analytics".

**FTS3 / WebFTS - A Powerful File Transfer Service for Scientific Communities**  
2015 · Procedia Computer Science · 10.1016/j.procs.2015.11.076

*Reason.* Same file-transfer service as the previous record (near-duplicate content, different venue); out-of-domain and also duplicated.

> In this article we describe this intuitive new interface, \"WebFTS\", which allows users to easily schedule and manage large data transfers right from the browser"; keywords "Data storage; File transfer; FTS3; WebFTS".

**FTS3 -A file transfer service for Grids, HPCs and Clouds**  
2015 · Proceedings of Science · (no DOI)

*Reason.* Grid data-transfer service and web front end; file transfer infrastructure is a domain unrelated to API/web-service testing or security.

> FTS3, the service responsible for globally distributing the majority of the LHC data across the WLCG infrastructure"; the only relevant mention is "accessed through our standards-compliant REST API" and a "zero configuration" deployment claim.

**Enabling complexity management through merging business process modeling with MBSE**  
2019 · Procedia CIRP · 10.1016/j.procir.2019.04.267

*Reason.* Model-based systems engineering for product development processes; no APIs, no web services, no mutation testing.

> This paper presents an approach for merging MBSE with business processes"; keywords "Complexity management; Integral product architecture; Model based systems engineering; Product development process".

**Conceptualizing Node.js Projects: A Graph-Oriented Technology-Specific Modeling Method**  
2023 · Lecture Notes in Information Systems and Organisation · 10.1007/978-3-031-32418-5_4

*Reason.* Domain-specific conceptual modeling for dependency and project management, unrelated to API security or mutation testing.

> a modeling method for managing Node.js projects dependencies by adding a semantic analysis layer ... knowledge-driven project management approach"; keywords "ADOxx; Dependency management; RDF

**Automated Network Planner Based on Digital Twin for Wavelength Division Multiplexing Network**  
2025 · Proceedings of the National Conference on Communications, NCC · 10.1109/ncc63735.2025.10983014

*Reason.* Optical-network planning, an area with no relation to API/web-service testing or security or to mutation testing.

> presents a network planning tool based on Digital Twin technology for Dense Wavelength Division Multiplexing (DWDM) networks"; keywords "DWDM; OTN; Transparent optical networks

**Teaching Guide for Beginnings in DevOps and Continuous Delivery in AWS Focused on the Society 5.0 Skillset**  
2022 · Revista Iberoamericana de Tecnologias del Aprendizaje · 10.1109/rita.2022.3217172

*Reason.* Software-engineering education and DevOps pedagogy; the REST API is only the course exercise artifact.

> presents a didactic guide that allows the adoption of good development practices, strengthening soft and technical skills ... within systems engineering programs"; keywords "teaching guide; society 50; CI; CD

**Conversation Disentanglement As-a-Service**  
2023 · 31st IEEE/ACM International Conference on Program Comprehension, ICPC 2023 · 10.1109/icpc58990.2023.00018

*Reason.* Program-comprehension and NLP tooling packaged as a RESTful micro-service, with no API security or testing contribution.

> Associating messages to conversations is called conversation disentanglement, a useful and necessary pre-processing step to analyze datasets of instant messages"; keywords "conversation disentanglement; instant messaging

