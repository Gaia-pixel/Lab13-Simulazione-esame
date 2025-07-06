import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.year = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.get_years()
        for y in years:
            # self._view._ddAnno.options.append(ft.dropdown.Option(y))
            self._view._ddAnno.options.append(ft.dropdown.Option(key = y, data = y, on_click= self.handleDDYearSelection))

        self._view.update_page()

    def handleDDYearSelection(self, e):
        self.year = e.control.data
        print (f"{self.year}")

    def handleCreaGrafo(self,e):
        if self.year is None:
            self._view._txt_result.controls.append(ft.Text("Anno non selezionato"))
            self._view.update_page()
            return
        self._model.buildGraph(self.year)

        numNodes, numEdges = self._model.getGraphDetails()
        bestD, score = self._model.getMigliore()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {numNodes} nodi e {numEdges} archi"))
        self._view._txt_result.controls.append(ft.Text(f"Miglior driver: {bestD} con punteggio : {score}"))

        self._view.update_page()


    def handleCerca(self, e):
        try:
            k = int(self._view._txtIntK.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(f"inserire un numero intero"))
            self._view.update_page()
            return
        if not self._model.graphExists():
            self._view._txt_result.controls.append(ft.Text(f"Creare il grafo"))
            self._view.update_page()
            return

        dreamT, score = self._model.getDreamT(k)
        self._view._txt_result.controls.append(ft.Text(f"tasso di sconfitta dream team : {score}, di seguito i driver coinvolti: "))
        for d in dreamT:
            self._view._txt_result.controls.append(ft.Text(f"{d}"))
        self._view.update_page()
