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
    parser.add_argument("--latency_3_5", type=int, default=0, help="Latency between machine 3 and 5")
    parser.add_argument("--latency_5_6", type=int, default=0, help="Latency between machine 5 and 6")
    parser.add_argument("--latency_cli", type=int, default=0, help="Latency between client and machine 0")
	
    parser.add_argument('--pPath0', type=int, default=80, help='Ratio (int 0-100) of memcached cache hit')
    parser.add_argument('--pPath1', type=int, default=15, help='Ratio (int 0-100) of memcached miss & mongodb hit')
    parser.add_argument('--pPath2', type=int, default=5, help='Ratio (int 0-100) of memcached miss & mongodb miss')

    parser.add_argument('--ngxThreads', type=int, default=8, help='Number of Nginx threads')
    parser.add_argument('--htThreads', type=int, default=8, help='Number of Home Timeline threads')
    parser.add_argument('--htRedisThreads', type=int, default=8, help='Number of Home Timeline Redis threads')
    parser.add_argument('--psThreads', type=int, default=8, help='Number of Post Storage threads')
    parser.add_argument('--mmcThreads', type=int, default=8, help='Number of Memcached threads')
    parser.add_argument('--mongoThreads', type=int, default=8, help='Number of MongoDB threads')
    parser.add_argument('--mongoIOThreads', type=int, default=8, help='Number of MongoDB IO threads')

    parser.add_argument('--ngxCores', type=int, default=4, help='Number of cores assigned to NGINX')
    parser.add_argument('--htCores', type=int, default=4, help='Number of cores assigned to Home Timeline')
    parser.add_argument('--htRedisCores', type=int, default=4, help='Number of cores assigned to Home Timeline Redis')
    parser.add_argument('--psCores', type=int, default=4, help='Number of cores assigned to Post Storage')
    parser.add_argument('--mmcCores', type=int, default=4, help='Number of cores assigned to Memcached')
    parser.add_argument('--mongoCores', type=int, default=4, help='Number of cores assigned to MongoDB')
    parser.add_argument('--mongoIOCores', type=int, default=4, help='Number of cores assigned to MongoDB IO')
    
    parser.add_argument('--machNxg', type=int, default=0, help='Machine ID where NGINX is deployed')
    parser.add_argument('--machHt', type=int, default=1, help='Machine ID where Home Timeline is deployed')
    parser.add_argument('--machHtRedis', type=int, default=2, help='Machine ID where Home Timeline Redis is deployed')
    parser.add_argument('--machPs', type=int, default=3, help='Machine ID where Post Storage is deployed')
    parser.add_argument('--machMmc', type=int, default=4, help='Machine ID where Memcached is deployed')
    parser.add_argument('--machMongo', type=int, default=5, help='Machine ID where MongoDB is deployed')
    parser.add_argument('--machMongoIO', type=int, default=6, help='Machine ID where MongoDB IO is deployed')
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

        # Call post_storage_memcached.py
        proc = subprocess.run(['python3', 'post_storage_memcached.py'])
        if proc.returncode == 0:
            print("post_storage_memcached.py successfully executed")

        # Call post_storage.py
        proc = subprocess.run(['python3', 'post_storage.py'])
        if proc.returncode == 0:
            print("post_storage.py successfully executed")

        # Call home_timeline.py
        proc = subprocess.run(['python3', 'home_timeline.py'])
        if proc.returncode == 0:
            print("home_timeline.py successfully executed")

        # Call home_timeline_redis.py
        proc = subprocess.run(['python3', 'home_timeline_redis.py'])
        if proc.returncode == 0:
            print("home_timeline_redis.py successfully executed")

        # Call post_storage_mongodb.py
        proc = subprocess.run(['python3', 'post_storage_mongodb.py'])
        if proc.returncode == 0:
            print("post_storage_mongodb.py successfully executed")

        # Call mongo_io.py
        proc = subprocess.run(['python3', 'mongo_io.py'])
        if proc.returncode == 0:
            print("mongo_io.py successfully executed")

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

def generate_machines(latency_0_1, latency_1_2, latency_1_3, latency_3_4, latency_3_5, latency_5_6, latency_cli):
    try:
        # Call machines.py
        proc = subprocess.run(['python3', 'machines.py', f"--latency_0_1={latency_0_1}", f"--latency_1_2={latency_1_2}", f"--latency_1_3={latency_1_3}", f"--latency_3_4={latency_3_4}", f"--latency_3_5={latency_3_5}", f"--latency_5_6={latency_5_6}", f"--latency_cli={latency_cli}"])
        if proc.returncode == 0:
            print("machines.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_graph(ngxThreads, htThreads, htRedisThreads, psThreads, mmcThreads, mongoThreads, mongoIOThreads, ngxCores, htCores, htRedisCores, psCores, mmcCores, mongoCores, mongoIOCores, machNxg, machHt, machHtRedis, machPs, machMmc, machMongo, machMongoIO):
    try:
        # Call graph.py
        proc = subprocess.run(['python3', 'graph.py', f"--ngxThreads={ngxThreads}", f"--htThreads={htThreads}", f"--htRedisThreads={htRedisThreads}", f"--psThreads={psThreads}", f"--mmcThreads={mmcThreads}", f"--mongoThreads={mongoThreads}", f"--mongoIOThreads={mongoIOThreads}", f"--ngxCores={ngxCores}", f"--htCores={htCores}", f"--htRedisCores={htRedisCores}", f"--psCores={psCores}", f"--mmcCores={mmcCores}", f"--mongoCores={mongoCores}", f"--mongoIOCores={mongoIOCores}", f"--machNxg={machNxg}", f"--machHt={machHt}", f"--machHtRedis={machHtRedis}", f"--machPs={machPs}", f"--machMmc={machMmc}", f"--machMongo={machMongo}", f"--machMongoIO={machMongoIO}"])
        if proc.returncode == 0:
            print("graph.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def generate_path(pPath0, pPath1, pPath2):
    try:
        # Call path.py
        proc = subprocess.run(['python3', 'path.py', f"--pPath0={pPath0}", f"--pPath1={pPath1}", f"--pPath2={pPath2}"])
        if proc.returncode == 0:
            print("path.py successfully executed")

    except FileNotFoundError as e:
        print(e)

def main():
    os.makedirs("json/microservice", exist_ok=True)
    args = parse_arguments()
    generate_microservices()
    generate_client(args.end_seconds, args.monitor_interval)
    generate_machines(args.latency_0_1, args.latency_1_2, args.latency_1_3, args.latency_3_4, args.latency_3_5, args.latency_5_6, args.latency_cli)
    generate_graph(args.ngxThreads, args.htThreads, args.htRedisThreads, args.psThreads, args.mmcThreads, args.mongoThreads, args.mongoIOThreads, args.ngxCores, args.htCores, args.htRedisCores, args.psCores, args.mmcCores, args.mongoCores, args.mongoIOCores, args.machNxg, args.machHt, args.machHtRedis, args.machPs, args.machMmc, args.machMongo, args.machMongoIO)
    generate_path(args.pPath0, args.pPath1, args.pPath2)

if __name__ == "__main__":
    main()