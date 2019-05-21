from django.shortcuts import render
from .PyDSSlite import PyDSS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoadGraphSerializer
from django.http import Http404
from .models import DssFiles
import pandas as pd

# Create your views here.
class pydss:
    def __init__(self, path):
        if path:
            self.Settings = {
                'Start Day'              : 1,
                'End Day'                : 365,
                'Hour'                   : 1,
                'Step resolution (min)'  : 1,
                'Max Control Iterations' : 50,
                'Simulation Type'        : 'Time series',
                'DSS File'               : path,
            }

            self.pydss = PyDSS.createInstance(self.Settings)
            self.dssGraph = self.pydss.graph()

    def CreateGlobalDataSource(self):
        self.clearData()
        for N1, N2 in self.dssGraph.edges():
            Xs = [self.dssGraph.node[N1]['X'], self.dssGraph.node[N2]['X']]
            Ys = [self.dssGraph.node[N1]['Y'], self.dssGraph.node[N2]['Y']]
            if 0 not in Xs and 0 not in Ys:
                V = ['%0.3f' % x for x in self.dssGraph.node[N2]['V']]
                VV = []
                VV.extend(self.dssGraph.node[N2]['V'])
                VV.extend(self.dssGraph.node[N1]['V'])
                VV = [x for x in VV if x != 0]
                self.Data['Class'].append(self.dssGraph[N1][N2]['Class'])
                self.Data['Name'].append(self.dssGraph[N1][N2]['Name'])
                self.Data['Xs'].append(Xs)
                self.Data['Ys'].append(Ys)
                self.Data['Phases'].append(self.toPhases(self.dssGraph.node[N1]['Phs']))
                self.Data['fromBus'].append(N1)
                self.Data['toBus'].append(N2)
                self.Data['X'].append(Xs[1])
                self.Data['Y'].append(Ys[1])
                self.Data['V'].append(V)
                self.Data['Vmax'].append(max(VV) if len(VV) > 0 else 0)
                self.Data['Vmin'].append(min(VV) if len(VV) > 0 else 0)
                self.Data['I'].append(self.dssGraph[N1][N2]['I'])
                self.Data['Imax'].append(self.dssGraph[N1][N2]['Imax'])
                self.Data['D'].append(self.dssGraph.node[N2]['D'])
                self.Data['kVbase'].append(self.dssGraph.node[N2]['kVbase'])
        # import pandas as pd
        # print(pd.DataFrame(self.Data))
#        self.source.data = self.Data
        for Node in self.dssGraph.nodes():
            self.NodeData['X'].append(self.dssGraph.node[Node]['X'])
            self.NodeData['Y'].append(self.dssGraph.node[Node]['Y'])
            self.NodeData['PV'].append(self.dssGraph.node[Node]['PV'])
            self.NodeData['Storage'].append(self.dssGraph.node[Node]['Storage'])

        # import pandas as pd
        # print(pd.DataFrame(self.NodeData))
#        self.sourceNode.data = self.NodeData

        return

    def clearData(self):
        self.Data = {
            'Class'   : [],
            'Name'    : [],
            'Xs'      : [],
            'Ys'      : [],
            'Phases'  : [],
            'fromBus' : [],
            'toBus'   : [],
            'X'       : [],
            'Y'       : [],
            'V'       : [],
            'D'       : [],
            'kVbase'  : [],
            'I'       : [],
            'Imax'    : [],
            'Vmax'    : [],
            'Vmin'    : [],
        }
#        self.source = ColumnDataSource(self.Data)

        self.NodeData = {
            'X': [],
            'Y': [],
            'PV': [],
            'Storage': [],
        }
 #       self.sourceNode = ColumnDataSource(self.NodeData)
#        self.SelectedNode = self.Data.copy()
        return

    def toPhases(self, phList):
        phases = ''
        if 0 in phList:
            phases+='A'
        if 1 in phList:
            phases+='B'
        if 2 in phList:
            phases+='C'
        return phases

class DssFileList(APIView):
    """List all available DSS files and their path"""
    def get(self, request, format=None):
        files = DssFiles.objects.all()
        serializer = LoadGraphSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LoadGraphSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoadGraphs(APIView):
    """
    Load the graph of a specific dss file
    """

    def get_obj(self, pk):
        try:
            return DssFiles.objects.get(pk=pk)
        except DssFiles.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        """
        Return a list of all users.
        """
        graph = self.get_obj(pk)
        serializer = LoadGraphSerializer(graph, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk, format=None):
        graph = self.get_obj(pk)
#        print(getattr(graph, 'path'))
        pydss_instance = pydss(getattr(graph, 'path'))
        pydss_instance.CreateGlobalDataSource()
#        serializer = LoadGraphSerializer(graph)
#        print(serializer.data)
        return Response(pydss_instance.Data)

    def delete(self, request, pk, format=None):
        graph = self.get_obj(pk)
        graph.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
