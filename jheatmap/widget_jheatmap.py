from IPython.html import widgets
import uuid
from IPython.utils.traitlets import Unicode
from IPython.display import display, Javascript
import pandas
import os



# Define our JHeatmap and its target model and default view.
TMP = "tmp"


class JHeatmap(widgets.DOMWidget):
    _view_name = Unicode('JHeatmapWidget', sync=True)

    def __init__(self, values_df: pandas.DataFrame,
                 rows: list=[],
                 cols: list=[],
                 init_config: str="",
                 **kwargs):
        """
        :type values_df: pandas.DataFrame
            :param values_df:
            :param rows:
            :param cols:
            :param init_config:
            :param kwargs:
            """
        super(JHeatmap, self).__init__(**kwargs)
        self._popup_shown = False
        self._popup = None
        values_df = self._primary_col(cols, values_df)
        values_df = self._primary_row(rows, values_df)

        self._tmp_file_values = self._get_tmp_filename(".values")

        values_df.to_csv(self._tmp_file_values, quoting=None, sep="\t", index=False, header=True)
        self._init_config = init_config


    @staticmethod
    def _primary_row(rows, values_df) -> pandas.DataFrame:
        if len(rows) != 0:
            df_columns = list(values_df.columns)
            row_primary = rows[0]
            if len(rows) > 0 and df_columns.index(row_primary) != 1:
                old_order = df_columns[1:]
                new_order = df_columns[:1]
                new_order.append(row_primary)
                old_order.remove(row_primary)
                new_order += old_order
                values_df = values_df[new_order]
        return values_df

    @staticmethod
    def _primary_col(cols, values_df) -> pandas.DataFrame:
        if len(cols) != 0:
            df_columns = list(values_df.columns)
            col_primary = cols[0]
            if df_columns.index(col_primary) != 0:
                old_order = df_columns
                old_order.remove(col_primary)
                new_order = [col_primary] + old_order
                values_df = values_df[new_order]
        return values_df

    @staticmethod
    def _get_tmp_filename(filename):
        tmp_base = "jheatmap-" + str(uuid.uuid1())
        if not os.path.exists(TMP):
            os.mkdir(TMP)
        return TMP + "/" + tmp_base + filename

    #def get_popup(self) -> widgets.PopupWidget:
    #    if self._popup is None:
    #        self._create_popup()
    #    return self._popup

    def exec_js(self, js):
        self.send({
            "action": "exec",
            "value": js
        })

    def _ipython_display_(self, **kwargs):
        # Show the widget, then send the current state
        #if self._popup is not None and not self._popup_shown:
        #   print("popup display!")
        #   self._popup_shown = True
        #   display(self._popup)
        #   return

        widgets.DOMWidget._ipython_display_(self, **kwargs)

        funcs = " heatmap.options.container[0]._heatmapInstance = heatmap; "
        if len(self._init_config) > 0:
            funcs += " " + self._init_config
        init = "init : function(heatmap) {" + funcs + "}"


        self.send({
            "action": "draw",
            "value": "{data : { values : new jheatmap.readers.TableHeatmapReader( { url : '" + self._tmp_file_values + "'} ) }, " + init + " }"
        })

    def show(self):
        display(self)

    def _create_popup(self):
        self._popup = widgets.PopupWidget()
        self._popup.description = "JHeatmap"
        self._popup.button_text = "Show heatmap"
        self._popup.children = [self]
        #self._popup.on_displayed(self._ipython_display_)


