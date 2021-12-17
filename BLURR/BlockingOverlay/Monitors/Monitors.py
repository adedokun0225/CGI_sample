from System.System import System
if System.isWindows():
    from BlockingOverlay.Monitors.Backends.Windows import enumerate_monitors
elif System.isMac():
    from BlockingOverlay.Monitors.Backends.OSX import enumerate_monitors
elif System.isLinux():
    from BlockingOverlay.Monitors.Backends.Linux import enumerate_monitors


class Monitors():

    def __init__(self):
        self.processedMonitors = []

    # deletes all the monitors that were stored as processed
    def reset(self):
        self.processedMonitors = []

    # returns (width, height) of the main monitor
    def getMainDims(self):
        monitors = list(enumerate_monitors())
        for monitor in monitors:
            if monitor.x == 0 and monitor.y == 0:
                return (monitor.width, monitor.height)

    # returns the geo strings for not processed monitors (never returns the main monitor)
    def getNewMonitors(self):
        monitors = list(enumerate_monitors())

        # find the main monitor
        mainMonitor = None
        for monitor in monitors:
            if monitor.x == 0 and monitor.y == 0:
                mainMonitor = monitor

        newGeos = []
        for monitor in monitors:

            # don't return the main monitor
            if monitor.x == 0 and monitor.y == 0:
                continue

            found = False
            for processedMonitor in self.processedMonitors:
                if monitor.x == processedMonitor.x and monitor.y == processedMonitor.y:
                    found = True
                    break

            # prepare the geo string for the new monitor
            if not found:

                # save the monitor as processed
                self.processedMonitors.append(monitor)

                # proper scaling (mainly for retarded windows)
                width = round(monitor.width /
                              monitor.scaling * mainMonitor.scaling)
                height = round(monitor.height /
                               monitor.scaling * mainMonitor.scaling)
                geo = str(width) + "x" + str(height)

                geoPos = ""
                if monitor.x < 0:
                    geoPos += str(int(monitor.x))
                else:
                    geoPos += "+" + str(int(monitor.x))

                if monitor.y < 0:
                    geoPos += str(int(monitor.y))
                else:
                    geoPos += "+" + str(int(monitor.y))

                geo += geoPos
                newGeos.append(geo)

        return newGeos
