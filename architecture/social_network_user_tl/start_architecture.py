# This file is used to generate the microservices, machines, graph and path for the 4-tier architecture
# The microservices are generated by calling the python files that generate the microservices
# The machines are generated by calling the corresponding file. There is a file for each network configuration
# The graph is generated by calling the graph.py file with the corresponding parameters (number of threads, cores and machines for each microservice)
# The path is generated by calling the path.py file

import subprocess
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a service graph with input arguments')
    parser.add_argument('--end_seconds', type=int, default=60, help='Epoch end time in seconds')
    parser.add_argument('--monitor_interval', type=int, default=0, help='Interval at which the client will monitor the system (in seconds)')

    parser.add_argument("--latency_0_1", type=int, default=0, help="Latency between machine 0 and 1")
    parser.add_argument("--latency_1_2", type=int, default=0, help="Latency between machine 1 and 2")
    parser.add_argument("--latency_1_3", type=int, default=0, help="Latency between machine 1 and 3")
    parser.add_argument("--latency_3_4", type=int, default=0, help="Latency between machine 3 and 4")
    parser.add_argument("--latency_1_5", type=int, default=0, help="Latency between machine 1 and 5")
    parser.add_argument("--latency_5_6", type=int, default=0, help="Latency between machine 5 and 6")
    parser.add_argument("--latency_5_7", type=int, default=0, help="Latency between machine 5 and 7")
    parser.add_argument("--latency_7_8", type=int, default=0, help="Latency between machine 7 and 8")

    parser.add_argument("--latency_cli", type=int, default=0, help="Latency between client and machine 0")
	
    parser.add_argument("--pPath0", type=int, default=64, help="Ratio (int 0-100) of redis hit & memcached cache hit")
    parser.add_argument("--pPath1", type=int, default=12, help="Ratio (int 0-100) of redis hit & memcached miss & mongodb hit")
    parser.add_argument("--pPath2", type=int, default=3, help="Ratio (int 0-100) of redis hit & memcached miss & mongodb miss")
    parser.add_argument("--pPath3", type=int, default=16, help="Ratio (int 0-100) of redis miss & memcached hit")
    parser.add_argument("--pPath4", type=int, default=3, help="Ratio (int 0-100) of redis miss & memcached miss & mongodb hit")
    parser.add_argument("--pPath5", type=int, default=2, help="Ratio (int 0-100) of redis miss & memcached miss & mongodb miss")

    parser.add_argument('--ngxThreads', type=int, default=8, help='Number of Nginx threads')
    parser.add_argument('--utThreads', type=int, default=8, help='Number of User Timeline threads')
    parser.add_argument('--utRedisThreads', type=int, default=8, help='Number of User Timeline Redis threads')
    parser.add_argument('--utMongoThreads', type=int, default=8, help='Number of User Timeline MongoDB threads')
    parser.add_argument('--utMongoIOThreads', type=int, default=8, help='Number of User Timeline MongoDB IO threads')
    parser.add_argument('--psThreads', type=int, default=8, help='Number of Post Storage threads')
    parser.add_argument('--psMmcThreads', type=int, default=8, help='Number of Post Storage Memcached threads')
    parser.add_argument('--psMongoThreads', type=int, default=8, help='Number of Post Storage MongoDB threads')
    parser.add_argument('--psMongoIOThreads', type=int, default=8, help='Number of Post Storage MongoDB IO threads')

    parser.add_argument('--ngxCores', type=int, default=4, help='Number of cores assigned to NGINX')
    parser.add_argument('--utCores', type=int, default=4, help='Number of cores assigned to User Timeline')
    parser.add_argument('--utRedisCores', type=int, default=4, help='Number of cores assigned to User Timeline Redis')
    parser.add_argument('--utMongoCores', type=int, default=4, help='Number of cores assigned to User Timeline MongoDB')
    parser.add_argument('--utMongoIOCores', type=int, default=4, help='Number of cores assigned to User Timeline MongoDB IO')
    parser.add_argument('--psCores', type=int, default=4, help='Number of cores assigned to Post Storage')
    parser.add_argument('--psMmcCores', type=int, default=4, help='Number of cores assigned to Post Storage Memcached')
    parser.add_argument('--psMongoCores', type=int, default=4, help='Number of cores assigned to Post Storage MongoDB')
    parser.add_argument('--psMongoIOCores', type=int, default=4, help='Number of cores assigned to Post Storage MongoDB IO')
    
    parser.add_argument('--machNxg', type=int, default=0, help='Machine ID where NGINX is deployed')
    parser.add_argument('--machUt', type=int, default=1, help='Machine ID where User Timeline is deployed')
    parser.add_argument('--machUtRedis', type=int, default=2, help='Machine ID where User Timeline Redis is deployed')
    parser.add_argument('--machUtMongo', type=int, default=3, help='Machine ID where User Timeline MongoDB is deployed')
    parser.add_argument('--machUtMongoIO', type=int, default=4, help='Machine ID where User Timeline MongoDB IO is deployed')
    parser.add_argument('--machPs', type=int, default=5, help='Machine ID where Post Storage is deployed')
    parser.add_argument('--machPsMmc', type=int, default=6, help='Machine ID where Post Storage Memcached is deployed')
    parser.add_argument('--machPsMongo', type=int, default=7, help='Machine ID where Post Storage MongoDB is deployed')
    parser.add_argument('--machPsMongoIO', type=int, default=8, help='Machine ID where Post Storage MongoDB IO is deployed')
    args = parser.parse_args()
    return args

# Generate microservices
def generate_microservices():
    try:
        #Call net_stack.py
        proc = subprocess.run(['python3', 'net_stack.py'])
        if proc.returncode == 0:
            print("net_stack.py successfully executed")

        # Call nginx.py
        proc = subprocess.run(['python3', 'nginx.py'])
        if proc.returncode == 0:
            print("nginx.py successfully executed")

        # Call user_timeline.py
        proc = subprocess.run(['python3', 'user_timeline.py'])
        if proc.returncode == 0:
            print("user_timeline.py successfully executed")

        # Call user_timeline_redis.py
        proc = subprocess.run(['python3', 'user_timeline_redis.py'])
        if proc.returncode == 0:
            print("user_timeline_redis.py successfully executed")
            
        # Call user_timeline_mongodb.py
        proc = subprocess.run(['python3', 'user_timeline_mongodb.py'])
        if proc.returncode == 0:
            print("user_timeline_mongodb.py successfully executed")

        # Call user_timeline_mongodb_io.py
        proc = subprocess.run(['python3', 'user_timeline_mongo_io.py'])
        if proc.returncode == 0:
            print("user_timeline_mongo_io.py successfully executed")

        # Call post_storage.py
        proc = subprocess.run(['python3', 'post_storage.py'])
        if proc.returncode == 0:
            print("post_storage.py successfully executed")

        # Call post_storage_memcached.py
        proc = subprocess.run(['python3', 'post_storage_memcached.py'])
        if proc.returncode == 0:
            print("post_storage_memcached.py successfully executed")

        # Call post_storage_mongodb.py
        proc = subprocess.run(['python3', 'post_storage_mongodb.py'])
        if proc.returncode == 0:
            print("post_storage_mongodb.py successfully executed")

        # Call post_storage_mongo_io.py
        proc = subprocess.run(['python3', 'post_storage_mongo_io.py'])
        if proc.returncode == 0:
            print("post_storage_mongo_io.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_client(end_seconds, monitor_interval):
    try:
        # Call client.py
        proc = subprocess.run(['python3', 'client.py', f"--end_seconds={end_seconds}", f"--monitor_interval={monitor_interval}"])
        if proc.returncode == 0:
            print("client.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_machines(latency_0_1, latency_1_2, latency_1_3, latency_3_4, latency_1_5, latency_5_6, latency_5_7, latency_7_8, latency_cli):
    try:
        # Call machines.py
        proc = subprocess.run(['python3', 'machines.py', f"--latency_0_1={latency_0_1}", f"--latency_1_2={latency_1_2}", f"--latency_1_3={latency_1_3}", f"--latency_3_4={latency_3_4}", f"--latency_1_5={latency_1_5}", f"--latency_5_6={latency_5_6}", f"--latency_5_7={latency_5_7}", f"--latency_7_8={latency_7_8}", f"--latency_cli={latency_cli}"])
        if proc.returncode == 0:
            print("machines.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_graph(ngxThreads, utThreads, utRedisThreads, utMongoThreads, utMongoIOThreads, psThreads, psMmcThreads, psMongoThreads, psMongoIOThreads, ngxCores, utCores, utRedisCores, utMongoCores, utMongoIOCores, psCores, psMmcCores, psMongoCores, psMongoIOCores, machNxg, machUt, machUtRedis, machUtMongo, machUtMongoIO, machPs, machPsMmc, machPsMongo, machPsMongoIO):
    try:
        # Call graph.py
        proc = subprocess.run(['python3', 'graph.py', f"--ngxThreads={ngxThreads}", f"--utThreads={utThreads}", f"--utRedisThreads={utRedisThreads}", f"--utMongoThreads={utMongoThreads}", f"--utMongoIOThreads={utMongoIOThreads}", f"--psThreads={psThreads}", f"--psMmcThreads={psMmcThreads}", f"--psMongoThreads={psMongoThreads}", f"--psMongoIOThreads={psMongoIOThreads}", f"--ngxCores={ngxCores}", f"--utCores={utCores}", f"--utRedisCores={utRedisCores}", f"--utMongoCores={utMongoCores}", f"--utMongoIOCores={utMongoIOCores}", f"--psCores={psCores}", f"--psMmcCores={psMmcCores}", f"--psMongoCores={psMongoCores}", f"--psMongoIOCores={psMongoIOCores}", f"--machNxg={machNxg}", f"--machUt={machUt}", f"--machUtRedis={machUtRedis}", f"--machUtMongo={machUtMongo}", f"--machUtMongoIO={machUtMongoIO}", f"--machPs={machPs}", f"--machPsMmc={machPsMmc}", f"--machPsMongo={machPsMongo}", f"--machPsMongoIO={machPsMongoIO}"])
        if proc.returncode == 0:
            print("graph.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_path(pPath0, pPath1, pPath2, pPath3, pPath4, pPath5):
    try:
        # Call path.py
        proc = subprocess.run(['python3', 'path.py', f"--pPath0={pPath0}", f"--pPath1={pPath1}", f"--pPath2={pPath2}", f"--pPath3={pPath3}", f"--pPath4={pPath4}", f"--pPath5={pPath5}"])
        if proc.returncode == 0:
            print("path.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def main():
    os.makedirs("json/microservice", exist_ok=True)
    args = parse_arguments()
    generate_microservices()
    generate_client(args.end_seconds, args.monitor_interval)
    generate_machines(args.latency_0_1, args.latency_1_2, args.latency_1_3, args.latency_3_4, args.latency_1_5, args.latency_5_6, args.latency_5_7, args.latency_7_8, args.latency_cli)
    generate_graph(args.ngxThreads, args.utThreads, args.utRedisThreads, args.utMongoThreads, args.utMongoIOThreads, args.psThreads, args.psMmcThreads, args.psMongoThreads, args.psMongoIOThreads, args.ngxCores, args.utCores, args.utRedisCores, args.utMongoCores, args.utMongoIOCores, args.psCores, args.psMmcCores, args.psMongoCores, args.psMongoIOCores, args.machNxg, args.machUt, args.machUtRedis, args.machUtMongo, args.machUtMongoIO, args.machPs, args.machPsMmc, args.machPsMongo, args.machPsMongoIO)
    generate_path(args.pPath0, args.pPath1, args.pPath2, args.pPath3, args.pPath4, args.pPath5)

if __name__ == "__main__":
    main()