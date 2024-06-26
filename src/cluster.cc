#include <time.h>

#include "cluster.hh"

Cluster::~Cluster() {
	srand(time(NULL));
	for(auto serv: services) 
		delete serv;
	for(auto ele: machineMap)
		delete ele.second;
}

unsigned
Cluster::getServId(const std::string& n) {
	assert(servNameIdMap.find(n) != servNameIdMap.end());
	return servNameIdMap[n];
}

MicroService*
Cluster::getService(const std::string& n) {
	unsigned index = getServId(n);
	return services[index];
}

void
Cluster::addService(MicroService* serv) {
	unsigned servId = services.size();
	services.push_back(serv);
	serv->setId(servId);
	servNameIdMap[serv->getName()] = servId;
	// std::pair<std::string, std::string> key = std::pair<std::string, std::string> (serv->getServName(), serv->getServDomain());
	std::string key = serv->getServName() + '_' + serv->getServDomain();
	if(servMap.find(key) == servMap.end())
		servMap[key] = std::vector<MicroService*>();
	servMap[key].push_back(serv);
}

void
Cluster::addEdge(std::string srcServ, std::string targServ, bool biDir) {
	assert(servNameIdMap.find(srcServ) != servNameIdMap.end());
	// std::cout << targServ << std::endl;
	assert(servNameIdMap.find(targServ) != servNameIdMap.end());
	MicroService* src = services[servNameIdMap[srcServ]];
	MicroService* targ = services[servNameIdMap[targServ]];
	src->addSendChn(targ);
	if(biDir)
		targ->addSendChn(src);
}

unsigned
Cluster::getNumService() {
	return services.size();
}

void 
Cluster::setServPath(std::vector<MicroServPath> path) {
	paths = path;
}

void
Cluster::setServPathDistr(std::vector<unsigned> dist) {
	assert(dist.size() == paths.size());
	unsigned accum = 0;
	for(unsigned prob: dist) {
		accum += prob;
		pathDistr.push_back(accum);
	}
	if(accum != 100) {
		printf("accum = %u\n", accum);
		printf("Error: all path probability do not sum up to 100\n");
		for(unsigned i = 0; i < dist.size(); ++i) {
			printf("Path %d probability: %d\n", i, dist[i]);
		}
		exit(1);
	}
	// assert(accum == 1.0);
}

void 
Cluster::addMachine(Machine* mac) {
	unsigned mid = mac->getId();
	assert(machineMap.find(mid) == machineMap.end());
	machineMap[mid] = mac;
}

Machine* 
Cluster::getMachine(unsigned mid) {
	auto itr = machineMap.find(mid);
	assert(itr != machineMap.end());
	return (*itr).second;
}

void
Cluster::setClientLat(Time lat) {
	clientNat = lat;
	machineMap[0]->setClientLat(lat);
}

Time
Cluster::getClientLat() {
	return clientNat;
}

void
Cluster::addMachinesLink(unsigned mid1, unsigned mid2, unsigned cap, Time lat) {
	Machine* mac1 = getMachine(mid1);
	Machine* mac2 = getMachine(mid2);
	mac1->addConn(mac2, lat);
	mac2->addConn(mac1, lat);
}

void
Cluster::setupConn() {
	for(auto it: machineMap) {
		it.second->setupConnections();
	}
}

void
Cluster::enqueue(Job* j) {
	// select a path for this job
	unsigned prob = rand() % 100;
	unsigned i = 0;
	while(pathDistr[i] < prob)
		++i;
	j->setPathNode(paths[i].getEntry());
	j->pathId = i;
	MicroServPathNode* node = paths[i].getEntry();
	// std::pair<std::string, std::string> key = std::pair<std::string, std::string> (node->getServName(), node->getServDomain());
	std::string key = node->getServName() + '_' + node->getServDomain();
	assert(servMap.find(key) != servMap.end());
	unsigned pos = rand() % servMap[key].size();
	// set visited
	j->setServId(node->getServName(), node->getServDomain(), servMap[key][pos]->getId());
	j->netSend = false;
	j->targServId = servMap[key][pos]->getId();
	// printf("In Cluster::enqueue set job: %d  set targServId: %d\n", j->id, j->targServId);	
	j->srcServId = unsigned(-1);
	j->newPathNode = true;
	servMap[key][pos]->getNet()->enqueue(j);
}

Time
Cluster::nextEventTime(Time globalTime) {
	return eventQueue->nextEventTime();
	// std::cout << "cluster next event time = " << time << std::endl;
}

// modify this to cope with ClientRxThread
void
Cluster::run(Time globalTime) {
	// std::cout << "cluster new round" << std::endl;
	// eventQueue->show();
	Event* e = eventQueue->pop();
	if(e == nullptr)
		return;
	e->run(globalTime);
	if(e->del)
		delete e;
	// nextServ->run(globalTime);
}

bool
Cluster::jobLeft() {
	if(eventQueue->nextEventTime() != INVALID_TIME) {
		std::cout << "Deadlock Check: Event Queue not empty" << std::endl;
		return false;
	}
	for(auto serv: services) {
		if(serv->jobLeft())
			return true;
	}
	return false;
}

void
Cluster::setFreq(const std::string& serv_name, unsigned freq) {
	for(MicroService* serv: services) {
		// std::cout << serv->getName() << std::endl;
		if(serv->getName() == serv_name)
			serv->setFreq(freq);
	}
}

// rapl
void 
Cluster::decServFreq(Time time, const std::string& serv_name) {
	// return;
	auto itr = services.begin();
	while(itr != services.end()) {
		const std::string& name = (*itr)->getServName();
		if(name.find(serv_name) != std::string::npos) {
			Event* event = new Event(Event::EventType::DEC_FREQ);
			event->time = time;
			(*itr)->insertEvent(event);
		}
		++itr;
	}

	// auto itr = servNameIdMap.find(serv_name);
	// assert(itr != servNameIdMap.end());

	// unsigned serv_id = itr->second;
	// Event* event = new Event(Event::EventType::DEC_FREQ);
	// event->time = time;
	// services[serv_id]->insertEvent(event);
}

void 
Cluster::incServFreq(Time time, const std::string& serv_name) {
	// return;
	auto itr = services.begin();
	while(itr != services.end()) {
		const std::string& name = (*itr)->getServName();
		if(name.find(serv_name) != std::string::npos) {
			Event* event = new Event(Event::EventType::INC_FREQ);
			event->time = time;
			(*itr)->insertEvent(event);
		}
		++itr;
	}

	// auto itr = servNameIdMap.find(serv_name);
	// assert(itr != servNameIdMap.end());

	// unsigned serv_id = itr->second;
	// Event* event = new Event(Event::EventType::INC_FREQ);
	// event->time = time;
	// services[serv_id]->insertEvent(event);
}

void 
Cluster::incServFreqFull(Time time, const std::string& serv_name) {
	// return;

	auto itr = services.begin();
	while(itr != services.end()) {
		const std::string& name = (*itr)->getServName();
		if(name.find(serv_name) != std::string::npos) {
			Event* event = new Event(Event::EventType::INC_FULL_FREQ);
			event->time = time;
			(*itr)->insertEvent(event);
		}
		++itr;
	}

	// auto itr = servNameIdMap.find(serv_name);
	// assert(itr != servNameIdMap.end());

	// unsigned serv_id = itr->second;
	// Event* event = new Event(Event::EventType::INC_FULL_FREQ);
	// event->time = time;
	// services[serv_id]->insertEvent(event);
}

void
Cluster::showCpuUtil(Time time) {
	for(MicroService* serv: services) {
		double util = serv->getCpuUtil(time);
		std::cout << serv->getName() << " cpu util = " << util << std::endl;
	}
}

void
Cluster::getPerTierTail(std::unordered_map<std::string, Time>& lat_info) {
	for(MicroService* serv: services) {
		Time lat = serv->getPercentileLat(0.99);
		serv->clearRespTime();
		lat_info[serv->getName()] = lat;
	}
}

void
Cluster::showStats(Time time) {
	// show stats per microservice
	// <<name: CPU; TX; avg; 20; 30; 50; 95; 99>>
	for(MicroService* serv: services) {
		if (serv->getName().find("net_stack") != std::string::npos)
			continue;
		double util = serv->getCpuUtil(time);
		uint64_t tx = serv->getTxRequests();
		std::cout << serv->getName() << ":" 
			<< util << ";" 
			<< tx/(time/1000000000.0) << ";" 
			<< serv->getAverageLat()/1000000.0 << ";"
			<< serv->getPercentileLat(0.2)/1000000.0 << ";"
			<< serv->getPercentileLat(0.3)/1000000.0 << ";" 
			<< serv->getPercentileLat(0.5)/1000000.0 << ";" 
			<< serv->getPercentileLat(0.95)/1000000.0 << ";" 
			<< serv->getPercentileLat(0.99)/1000000.0 << ";" << std::endl;

		std::unordered_map<int, uint64_t> txPath = serv->getTxRequestsPerPath();
		for (auto it = txPath.begin(); it != txPath.end(); ++it) {
			std::cout << serv->getName() << it->first << ":" 
			<< it->second/(time/1000000000.0) << ";" 
			<< serv->getAverageLatPerPath()[it->first]/1000000.0 << ";"
			<< serv->getPercentileLatPerPath(0.2)[it->first]/1000000.0 << ";"
		 	<< serv->getPercentileLatPerPath(0.3)[it->first]/1000000.0 << ";" 
			<< serv->getPercentileLatPerPath(0.5)[it->first]/1000000.0 << ";" 
		 	<< serv->getPercentileLatPerPath(0.95)[it->first]/1000000.0 << ";" 
			<< serv->getPercentileLatPerPath(0.99)[it->first]/1000000.0 << ";" << std::endl;
		}
		serv->clearRespTime();
	}
}

