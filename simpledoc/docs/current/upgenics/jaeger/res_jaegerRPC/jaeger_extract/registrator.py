import socket
import json
import requests
import threading
import time

# change service name according to your service,
service_name = "JobApplicationManagementAPI"

# change port number according to your service,
# do not add more than 1 port here
# do not add more than 1 port here
# do not add more than 1 port here
# do not add more than 1 port here
# do not add more than 1 port here
container_ports = ["5000"]

# change bellow to your service prefixes
api_prefixes = ["jobs"]

# alias of host
host_alias = "candidatejobapplicationmanagementapi"


class Kong_Registrar_For_Upstream(object):
    # When running in docker swarm or in container this class will
    # configure / create up-streams on kong when ever the container
    # is initiated / orchastread.

    service_name = ""
    container_ports = []

    kong_admin_url = ""
    kong_admin_upstream_url = ""
    kong_upstream_url = ""
    kong_admin_targets_url = ""
    kong_target_url = ""

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("hostname is:" + hostname)
    print("IP Address is:" + IPAddr)
    host_alias = ""

    def __init__(self, service_name, container_ports, host_alias):
        self.service_name = service_name
        self.host_alias = host_alias
        self.container_ports = container_ports
        self.kong_admin_url = "http://kong:8001/"
        self.kong_admin_upstream_url = self.kong_admin_url + "upstreams/"
        self.kong_upstream_url = self.kong_admin_upstream_url + host_alias + "/"
        self.kong_admin_targets_url = self.kong_upstream_url + "targets/"
        self.kong_target_url = self.kong_admin_targets_url + self.IPAddr

    def add_upstream(self, name, alias):
        r = requests.post(self.kong_admin_upstream_url,
                          json={
                              'name': alias,
                              "healthchecks": {"active": {"healthy": {"interval": 5}, "unhealthy": {"interval": 10, "tcp_failures": 1, "timeouts": 5}}}
                          }, verify=False)

        if r.status_code == 409:
            print("got 409 on adding upstream.")
            r = requests.get(self.kong_upstream_url, verify=False)

        if r.status_code == 200 or r.status_code == 201:
            print("upstream added.")
        else:
            # error log
            print("Error in upstream :" + str(r.status_code) + " : " + r.content)
            pass

    def check_target_exists(self, target):

        print("Checking if target " + target + " exists :")
        r = requests.get(self.kong_admin_targets_url + "?target=" + target)
        print(r.content)
        print(r.status_code)

        data = json.loads(r.content)

        for d_target in data["data"]:
            print("comparing target " + d_target["target"] + " == " + target)
            if d_target["target"] == target:
                return True

        return False

    def add_target(self, target, weight=100):
        if self.check_target_exists(target):
            print(target + " target already exists.")
            return True

        r = requests.post(self.kong_admin_targets_url, json={
            'target': target, "weight": weight}, verify=False)

        if r.status_code == 409:
            r = requests.get(self.kong_target_url, verify=False)

        if r.status_code == 200 or r.status_code == 201:
            print("target added.")
        else:
            # error log
            print("Error in adding target :" + r.status_code)
            pass

    def remove_unhealthy_targets_from_kong(self):
        try:
            print("Checking for unhealthy targets.")
            r = requests.get(self.kong_upstream_url + "health/",
                             headers={"Content-Type": "application/json"})
            print("response status code : " + str(r.status_code))
            print("response content : " + r.text)

            data = json.loads(r.text)

            for target in data["data"]:
                print("target : " +
                      str(target["health"]) + " - " + str(target["target"]))

                if(target["health"] == "UNHEALTHY"):
                    r = requests.delete(
                        self.kong_admin_targets_url + target["target"], headers={"Content-Type": "application/json"})
                    if r.status_code == 204:
                        print("UNHEALTHY Target Removed : " + target["target"])

        except Exception as ex:
            print(str(ex))

    def setup(self):
        upstream_response = requests.get(self.kong_upstream_url)

        self.remove_unhealthy_targets_from_kong()

        print(str(upstream_response.content))

        if "not found" in str(upstream_response.content).lower():
            # create upstream
            self.add_upstream(self.service_name, self.host_alias)

        for port in self.container_ports:
            self.add_target(self.IPAddr + ":" + port)


class Kong_Registrar_For_Routes(object):
    service_name = ""
    api_prefixes = []
    container_port = ""

    kong_admin_url = ""
    kong_admin_services_url = ""
    kong_service_url = ""
    kong_admin_route_url = ""
    host_alias = ""

    def __init__(self, service_name, container_port, api_prefixes, host_alias):
        self.service_name = service_name
        self.api_prefixes = api_prefixes
        self.container_port = container_port

        self.kong_admin_url = "http://kong:8001/"
        self.kong_admin_services_url = self.kong_admin_url + "services/"
        self.kong_service_url = self.kong_admin_services_url + service_name + "/"
        self.kong_admin_route_url = self.kong_service_url + "routes/"

        self.host_alias = host_alias

    def check_service_exists(self):
        print("Checking if service exists.")
        r = requests.get(self.kong_service_url)
        if r.status_code == 200:
            print(r.content)
            print("Service exists.")
            return True

        print("Service does not exists.")
        return False

    def check_route_exists(self, route_name):
        print("Checking if route exists.")
        r = requests.get(self.kong_admin_route_url +
                         "/" + route_name+"_wildcard" + "/service")
        if r.status_code == 200:
            print(r.content)
            print("Route exists.")
            return True

        print("Route does not exists.")
        return False

    def create_service(self):
        #hostname = socket.gethostname()

        # IPAddr = socket.gethostbyname(hostname)

        r = requests.post(self.kong_admin_services_url,
                          json={
                              "name": self.service_name,
                              "host": self.host_alias,
                              "port": int(self.container_port),
                              "path": "/",
                              "protocol": "http"
                          })

        if r.status_code == 200 or r.status_code == 201:
            print(r.content)
            return True

        print("error in creating service: " + str(r.status_code))
        return False

    def create_route(self, route_name):
        print("Creating route.")
        path = ["/"+route_name+"/*"]
        if route_name == "":
            path = ["/*"]

        r_name = route_name.replace("/", "_")

        r = requests.post(self.kong_admin_route_url,
                          json={
                              "name": r_name + "_wildcard",
                              "methods": ["GET", "POST", "OPTIONS"],
                              "paths": path,
                              "strip_path": False
                          })

        if r.status_code == 200 or r.status_code == 201:
            print(r.content)
            print("Route Created.")
            return True

        print("error in creating route: " +
              str(r.status_code) + str(r.content))
        return False

    def setup(self):
        if self.check_service_exists() == False:
            self.create_service()

        if len(api_prefixes) == 1 and api_prefixes[0] == "":
            self.create_route("")
            return

        for endpoint in api_prefixes:
            if self.check_route_exists(endpoint) == False:
                self.create_route(endpoint)


def register_upstreams_and_routes():
    kong_status = 404
    while kong_status != 200:
        try:
            r = requests.get("http://kong:8001/")
            kong_status = r.status_code
            if(r.status_code == 200):
                break
        except Exception as ex:
            print(str(ex))

        print("waiting for kong to start.")
        time.sleep(10)

    while True:
        print("UPDATING STREAMS AND ROUTES.")

        route_registrar = Kong_Registrar_For_Routes(
            service_name, container_ports[0], api_prefixes, host_alias)
        route_registrar.setup()

        upstream_registrar = Kong_Registrar_For_Upstream(
            service_name, container_ports, host_alias)
        # upstream_registrar.setup()

        print("DONE UPDATING STREAMS AND ROUTES.")

        time.sleep(60)


x = threading.Thread(target=register_upstreams_and_routes)
x.start()