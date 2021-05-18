from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

#Ideja
#Uzmi sve objekte ubaci u listu
#Sve koji imaju public i private u sebi
#Osim onog paola jednog
#isto sve ovo kao dole, samo kad zavrsis, izbacis ih iz liste

def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


try:
    connection = SmartConnectNoSSL(host="siriuslabvcenterserver.siriuscom.lab", user="USERNAME", pwd='PASSWORD')
    networks = connection.content.rootFolder.childEntity[0].networkFolder.childEntity
    DSwitch_FrontEnd = networks[-2]
    Portgroups2 = DSwitch_FrontEnd.portgroup
    #print("Ovo je tip: " + str(type(portgroups)))

    content = connection.RetrieveContent()
    dvs = get_obj(content, [vim.DistributedVirtualSwitch], 'DSwitch-FrontEnd') #sifra za vrata 7788#


    publicFolderCount = 0


    Portgroups = sorted(Portgroups2, key=lambda x: x.name)

    userNetwork = -1

    while userNetwork < len(Portgroups)-1:
        userNetwork = userNetwork + 1
        userNetworkAgain = userNetwork - 3
        try:
            fullFolderName = Portgroups[userNetwork].name.split(sep="-", maxsplit=1)
            if fullFolderName[1] == "Public":
                publicFolderCount = publicFolderCount + 1
                vlanId = Portgroups[userNetwork].config.defaultPortConfig.vlan.vlanId
                print("------------\n" + Portgroups[userNetwork].name + ", VLANid = " + str(vlanId) + " --------> public folder broj: " + str(publicFolderCount))

                brojac = 0

                while userNetworkAgain < len(Portgroups) - 1:
                    userNetworkAgain = userNetworkAgain + 1
                    if (fullFolderName[0] + "-Private" in Portgroups[userNetworkAgain].name):

                        distributedVirtualPortGroup = get_obj(content, [vim.dvs.DistributedVirtualPortgroup], Portgroups[userNetworkAgain].name)
                        #print("da li su isti???????")
                        #print(str(distributedVirtualPortGroup))
                        #print('-------------------------------------------------------------------------------------------')
                        #print(str(Portgroups[userNetworkAgain]))

                        spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
                        spec.configVersion = Portgroups[userNetworkAgain].config.configVersion
                        spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
                        spec.defaultPortConfig.vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()

                        if Portgroups[userNetworkAgain].name[-1] == "1":
                            print(Portgroups[userNetworkAgain].name + ", VLANid = " + str(vlanId - 200))
                            spec.defaultPortConfig.vlan.vlanId = vlanId - 200
                        else:
                            print(Portgroups[userNetworkAgain].name + ", VLANid = " + str(vlanId + 200))
                            spec.defaultPortConfig.vlan.vlanId = vlanId + 200

                        spec.defaultPortConfig.vlan.inherited = False

                        task = distributedVirtualPortGroup.ReconfigureDVPortgroup_Task(spec)
                        brojac = brojac + 1
                        if brojac == 2:
                            break
        except:
            print(Portgroups[userNetwork].name + " --> Ovde nesto ne valja") # There is one folder 'DPortGrouptest'
            #And paul.slowley user that has only public folder


    print("Kraj!!!")
except:
    print('Doslo je do Exceptiona')



Disconnect(connection)


'''
spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
spec.configVersion = '6'
spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
spec.defaultPortConfig.vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
spec.defaultPortConfig.vlan.vlanId = 500
spec.defaultPortConfig.vlan.inherited = False
managedObject.ReconfigureDVPortgroup_Task(spec)
'''