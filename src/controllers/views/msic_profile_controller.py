import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.SeqFeature import CompoundLocation
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from controllers.views.plot_creation_controller import PlotCreationController
from contextlib import contextmanager

class MSICProfileController(PlotCreationController):
    def __init__(self, main_ctrl):
        super().__init__(main_ctrl)
        self.main_ctrl = main_ctrl
        
        self.view = None
        
        self.genbank_uploaded = False
        self.genbank_links = {}
        
        self.update_timer = None
        
        self.plot_config_data = {}
        self.default_plot_config_data = {}
        self.plot_settings_data = {}
        
        self._suppress_traces = False

        
    def connect_view(self, view):
        self.view = view
        
    # Limits the line width values to the range [1;2]
    def validate_width(self, P):
        if P == "":
            return True
        if len(P) > 4:
            return False
        try:
            if float(P) <= 2 and float(P) >= 0:
                return True
            else: 
                return False
        except ValueError:
            return False
        
    # Limits values to positive integers
    def validate_positive_int(self, P):
        if P == "":
            return True
        try:
            if int(P) > 0:
                return True
            else: 
                return False
        except ValueError:
            return False
        
    def get_plot(self, df, csv_path, default_plot_config=False, genbank_file=None):
        df["position_region"] = np.arange(len(df))
        
        if genbank_file:
            seq = "".join(df["ref"].astype(str)).upper()
            gbk_record = SeqIO.read(genbank_file, "genbank")

            gbk_seq = str(gbk_record.seq).upper()
            
            # Match GenBank sequence
            match_start = seq.find(gbk_seq)
            
            gbk_region_start = match_start + 1
            
            ann = pd.DataFrame({
                "position_region": df["position_region"].values,
                "region_type_coarse": "intergenic",
                "region_type_fine": "intergenic"
            })
            ann["priority"] = 0

            gene_mask = ann["position_region"]
            ann.loc[gene_mask, "region_type_coarse"] = "gene_body"
            ann.loc[gene_mask, "region_type_fine"] = "gene_body"
            
            feature_priority = {
                "CDS": 5,
                "5'UTR": 4,
                "3'UTR": 4,
                "exon": 3,
                "intron": 2
            }

            for feat in gbk_record.features:
                ftype = feat.type
                if ftype not in ["CDS", "5'UTR", "3'UTR", "exon", "intron"]:
                    continue

                for start_local, end_local in self.extract_ranges(feat):
                    region_start = self.gbk_local_to_region(start_local, gbk_region_start)
                    region_end   = self.gbk_local_to_region(end_local, gbk_region_start)

                    low = min(region_start, region_end)
                    high = max(region_start, region_end)

                    mask = ann["position_region"].between(low, high)
                    pr = feature_priority[ftype]

                    overwrite = mask & (ann["priority"] < pr)
                    ann.loc[overwrite, "region_type_coarse"] = ftype
                    ann.loc[overwrite, "region_type_fine"] = ftype
                    ann.loc[overwrite, "priority"] = pr

            ann["region_type_simple"] = ann["region_type_coarse"].apply(self.simplify_region)
            
            merged = df.merge(
                ann.drop(columns="priority"),
                on="position_region",
                how="left",
                validate="one_to_one"
            )
            
            if self.view.reverse_ann.get():
                plot_df = merged[::-1].copy()
                plot_df["position_region"] = range(len(plot_df))
            else:
                plot_df = merged
            
            region_colors = {
                "CDS": "lightgreen",
                "UTR": "gold",
                "intron": "lightblue"
            }
            
        rolling_line_width = float(self.view.width_var.get())
        rolling_window = int(self.view.window_var.get())
        rolling_step = int(self.view.step_var.get())
    
        colors = []
        
        df['MSIC_rolling'] = df['MSIC'].rolling(window=rolling_window, center=True, min_periods=1).mean()
        
        df_sliced = df.iloc[::rolling_step]
    
        for value in df["MSIC"].tolist():
            if value >= 0.5:
                colors.append("green")
            elif value <= -0.5:
                colors.append("red")
            else:       
                colors.append("#DCDCDC80")
                
        fig, ax = plt.subplots(figsize=(13*self.main_ctrl.height_quo, 5.5*self.main_ctrl.height_quo))
        
        match self.view.plot_type_selection.get():
            case "scatter plot":
                ax.scatter(
                    x=df.index,
                    y=df["MSIC"],
                    color=colors,
                    s=20/(len(df)/500)
                )
            case "bar plot":
                ax.bar(
                    x=df.index,
                    height=df['MSIC'],
                    color=colors,
                    width=1.0
                ) 
            case "vertical line plot":
                ax.vlines(
                    x=df.index,
                    ymin=0,
                    ymax=df["MSIC"],
                    colors=colors,
                    linewidth=1.0
                )

        ax.set_ylim(-1, 1)

        df_sliced.reset_index().plot.line(
            x='index',
            y='MSIC_rolling',
            color='black',
            linewidth=rolling_line_width,
            ax=ax,
            legend=False
        )
        
        ax.axhline(y=0, color="blue", linewidth=0.5)
        
        legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=6, alpha=0.5, label="-0.5 < MSIC < 0.5"),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=6, alpha=0.8, label="MSIC >= 0.5"),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=6, alpha=0.8, label="MSIC <= -0.5"),
                Line2D([0], [0], color='black', lw=1.5, label="rolling mean"),
        ]
        
        if genbank_file:
            start_idx = 0
            current_region = plot_df.iloc[0]["region_type_simple"]
            
            for i in range(1, len(plot_df)):
                region_i = plot_df.iloc[i]["region_type_simple"]
                if region_i != current_region:
                    x0 = plot_df.iloc[start_idx]["position_region"]
                    x1 = plot_df.iloc[i - 1]["position_region"]
                    if current_region in region_colors:
                        ax.axvspan(x0, x1, color=region_colors[current_region], alpha=0.22)
                    start_idx = i
                    current_region = region_i

            x0 = plot_df.iloc[start_idx]["position_region"]
            x1 = plot_df.iloc[-1]["position_region"]
            if current_region in region_colors:
                ax.axvspan(x0, x1, color=region_colors[current_region], alpha=0.22)
                
            legend_elements.extend([
                Patch(facecolor="lightgreen", edgecolor="none", alpha=0.22, label="CDS"),
                Patch(facecolor="gold", edgecolor="none", alpha=0.22, label="UTR"),
                Patch(facecolor="lightblue", edgecolor="none", alpha=0.22, label="intron"),
            ])
        
        fig.subplots_adjust(bottom=0.2, top=0.9)    
        
        if self.plot_config_data and csv_path in self.plot_config_data and not default_plot_config:
            fig.subplots_adjust(**self.plot_config_data[csv_path]["subplot_params"])
            ax.set_xlim(**self.plot_config_data[csv_path]["xlims"])
            ax.set_ylim(**self.plot_config_data[csv_path]["ylims"])
        if csv_path not in self.plot_config_data:
            self.update_plot_config(ax=ax, fig=fig, file_path=csv_path, default_values=True)
        if default_plot_config:
            fig.subplots_adjust(**self.default_plot_config_data[csv_path]["subplot_params"])
            ax.set_xlim(**self.default_plot_config_data[csv_path]["xlims"])
            ax.set_ylim(**self.default_plot_config_data[csv_path]["ylims"])
                    
        fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 0.08), ncol=4, frameon=False)
        
        return fig, ax
    
    def preview_plot(self, csv_path=None):
        if len(self.file_list) == 0:
            self.view.show_no_file_error()
            return
        
        if csv_path == None:
            self.csv_index = 0
            csv_path = self.file_list[0]
        
        if self.fig:
            self.ax.clear()
            plt.close(self.fig)
            self.ax = None
            self.fig = None
        
        for plot in self.view.plot_frame.winfo_children():
            plot.destroy()
        try:
            self.view.toolbar.destroy()
        except:
            pass
        
        with open(csv_path, "r") as csv_file:
            df = pd.read_csv(csv_file)
            
        genbank_file = None
            
        for key in self.genbank_links.keys():
            if csv_path in self.genbank_links[key]:
                genbank_file = key
                break
        
        with self.silence_traces():
            if self.plot_settings_data and csv_path in self.plot_settings_data:
                self.view.step_var.set(self.plot_settings_data[csv_path]["step_size"])
                self.view.window_var.set(self.plot_settings_data[csv_path]["window_size"])
                self.view.width_var.set(self.plot_settings_data[csv_path]["line_width"])
                self.view.plot_type_selection.set(self.plot_settings_data[csv_path]["plot_type"])
            else:
                self.view.step_var.set(1)
                self.view.window_var.set(20)
                self.view.width_var.set(1)
                self.view.plot_type_selection.set("scatter plot")  
            
        self.fig, self.ax = self.get_plot(df, csv_path, genbank_file)
        
        base_string = df["ref"].str.cat()
        msic_scores = list(df["MSIC"])
                
        self.view.show_interactive_view(self.fig)

        self.view.canvas.mpl_connect("draw_event", lambda e: self.update_plot_config(ax=self.ax, fig=self.fig, event=e, file_path=csv_path))
        self.view.canvas.mpl_connect("scroll_event", self.plot_zoom(ax=self.ax))
        self.view.canvas.mpl_connect("motion_notify_event", lambda e: self.plot_hover_event(e, self.ax, base_string, msic_scores))
        
    @contextmanager
    def silence_traces(self):
        self._suppress_traces = True
        try:
            yield
        finally:
            self._suppress_traces = False
        
    def update_plot(self, *args):      
        if self._suppress_traces:
            return
           
        if self.update_timer is not None:
            self.view.after_cancel(self.update_timer)
            self.update_timer = None
        if self.update_timer is None and self.fig is not None:
            self.update_timer = self.view.after(700, lambda: self.preview_plot(self.file_list[self.csv_index]))     
            
    def update_plot_settings(self, *args):
        if self._suppress_traces:
            return
        
        step_size = int(self.view.step_var.get())
        window_size = int(self.view.window_var.get())
        line_width = float(self.view.width_var.get())
        plot_type = self.view.plot_type_selection.get() 
        
        self.plot_settings_data[self.file_list[self.csv_index]] = {
            "step_size": step_size,
            "window_size": window_size,
            "line_width": line_width,
            "plot_type": plot_type
        }
        
           
    # Returns the current subplot spacing parameters as a dictionary
    def update_plot_config(self, file_path, ax, fig, default_values=False, event=None):
        if fig is not None:
            pars = fig.subplotpars
            subplot_params = {
                "left": pars.left,
                "right": pars.right,
                "bottom": pars.bottom,
                "top": pars.top,
                "wspace": pars.wspace,
                "hspace": pars.hspace,
            }
        
        if ax is not None:
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            
            xlims = {
                "left": xmin,
                "right": xmax
                
            }
            ylims = {
                "bottom": ymin,
                "top": ymax
            }
        
        if not default_values:
            self.plot_config_data[file_path] = {
                "subplot_params": subplot_params,
                "xlims": xlims,
                "ylims": ylims
            }
        else:
            self.default_plot_config_data[file_path] = {
                "subplot_params": subplot_params,
                "xlims": xlims,
                "ylims": ylims
            }
            
                                
    def plot_zoom(self, ax, base_scale=1.1):
        def zoom_ev(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            
            if event.button == 'up': 
                scale_factor = 1 / base_scale
            elif event.button == 'down': 
                scale_factor = base_scale
            else: 
                return

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            
            middle_x = ax.get_xlim()[1]-(ax.get_xlim()[1]-ax.get_xlim()[0])/2
            middle_y = ax.get_ylim()[1]-(ax.get_ylim()[1]-ax.get_ylim()[0])/2
            self.view.apply_zoom(ax, middle_x, middle_y, new_width, new_height)

        return zoom_ev

    def plot_hover_event(self, event, ax, base_string, msic_scores):
        if event.inaxes == ax:
            x = self.view.winfo_pointerx() - self.view.winfo_rootx() + 15
            y = self.view.winfo_pointery() - self.view.winfo_rooty() + 10
            
            scaled_x = x / self.main_ctrl.height_quo
            scaled_y = y / self.main_ctrl.height_quo
            
            if round(event.xdata) < len(msic_scores) and 0 <= round(event.xdata):
                msic = round(msic_scores[round(event.xdata)], 4)
            else:
                msic = "-"
            
            self.view.show_tooltip(event.xdata, str(msic), scaled_x, scaled_y)
            self.view.update_base_bar(base_string, round(event.xdata))
        else:
            self.view.tooltip.place_forget()
    
    def extract_ranges(self, feature):
        loc = feature.location
        if isinstance(loc, CompoundLocation):
            parts = loc.parts
        else:
            parts = [loc]

        ranges = []
        for part in parts:
            start = int(part.start) + 1   # convert 0-based to 1-based
            end = int(part.end)           # inclusive in 1-based
            ranges.append((start, end))
        return ranges
    
    def gbk_local_to_region(self, local_pos, gbk_region_start):
        return gbk_region_start + local_pos - 1
    
    def simplify_region(self, x):
        if x == "CDS":
            return "CDS"
        elif x in ["5'UTR", "3'UTR"]:
            return "UTR"
        elif x == "intron":
            return "intron"
        elif x == "upstream":
            return "upstream"
        elif x == "downstream":
            return "downstream"
        else:
            return x
        
    def region_to_gene_5to3(self, position_region, gene_start_region, gene_end_region, strand):
        if gene_start_region <= position_region <= gene_end_region:
            if strand == "+":
                return position_region - gene_start_region + 1
            elif strand == "-":
                return gene_end_region - position_region + 1
        return np.nan