# Shows how to read simulation results.
# For more help see 'iesve.ResultsReader'

# Modules to import
import numpy as np
import pandas as pd
import sys
import iesve
import plotly.graph_objects as go
from ies_file_picker import IesFilePicker

from pprint import pprint
from tabulate import tabulate
import csv

# Functions to use
def sum_convert(result_reader, aps_data, type):
    """
    This sums the results and converts them to kWh if required.
    """
    # check if the read was successful
    if aps_data is None:
        return np.nan # represents no data

    # sum and convert
    sum = np.sum(aps_data)
    sum = sum * (24 / result_reader.results_per_day) # hourly
    if type is 'e':
        sum = sum / 1000.0 # kWh

    # clean up memory for the results array
    del aps_data
    return sum

def read_sum_convert(result_reader, use_id = iesve.EnergyUse.unspecified, src_id = iesve.EnergySource.unspecified, met_id = iesve.EnergyMeter.unspecified, type = 'e', add_subs = -1):
    """
    This reads the variable defined by use_id, src_id and met_id from
    the result_reader.
    It then sums the results and converts them to kWh if required.
    """
    start_day = -1
    end_day = -1
    aps_data = result_reader.get_energy_results(use_id, src_id, met_id, type, add_subs, start_day, end_day)
    return sum_convert(result_reader, aps_data, type)


# Code to execute
if __name__ == "__main__":
    
    # Open APS file:
    file_name = IesFilePicker.pick_aps_file()
    if (file_name is not None) and (len(file_name) > 0):
        
        results_file_reader = iesve.ResultsReader.open(file_name)
        assert results_file_reader is not None, "Error opening results file"

        # Settings
        type = 'e'                      # Output result type: 'e'nergy or 'c'arbon
        used = True                     # Retrieve only Energy Uses, Source and Meters that have data
        show_uses = True               # Display Energy Uses Info
        show_sources = False            # Display Energy Sources Info
        show_meters = True             # Display Energy Meters Info
        show_source_matrix = True       # Display Energy Use Matrix by Source
        show_meter_matrix = False       # Display Energy Use Matrix by Meter
        show_groupings = True           # Display Example groupings
        
        # Table fomratting (see tabulate)
        tablefmt = "grid"
        headers = "firstrow"
        numalign = "decimal"
        floatfmt = "6.3f"
        
        # Display Energy Uses Info
        map_uses = results_file_reader.get_energy_uses( used )
        if show_uses is True:
            print("\n=== Energy Uses ===\n")
            pprint( map_uses, width=256 )
            print("\n===================\n")
        all_uses = list( map_uses.values() )
        all_uses.append({ 'id' : iesve.EnergyUse.unspecified, 'name' : "Total" }) # unspecified will give us the total
        print(all_uses)
        
        # Display Energy Sources Info
        map_srcs = results_file_reader.get_energy_sources( used )
        if show_sources is True:
            print("\n=== Energy Sources ===\n")
            pprint( map_srcs, width=256 )
            print("\n======================\n")
        all_srcs = list( map_srcs.values() )
        all_srcs.append({ 'id' : iesve.EnergySource.unspecified, 'name' : "Total" }) # unspecified will give us the total
        
        
        # Display Energy Meters Info
        map_mets = results_file_reader.get_energy_meters( used )
        if show_meters is True:
            print("\n=== Energy Meters ===\n")
            pprint( map_mets, width=256 )
            print("\n=====================\n")
        all_mets = list( map_mets.values() )
        all_mets.append({ 'id' : iesve.EnergyMeter.unspecified, 'name' : "", 'source_id' : iesve.EnergySource.unspecified }) # unspecified will give us the total
        
        # Set display units
        units = "kgC" if type is 'c' else "kWh"
        
        # Create Energy Use Matrix by Source
        if show_source_matrix is True:
            print("\n=== Energy Source Matrix ===\n")
            tbl_src = []
            tbl_row = [ units ]
            tbl_rows=[]
            for use in all_uses:
                tbl_row.append( use['name'] )
                tbl_rows.append( use['name'] )
            tbl_src.append( tbl_row )
            print(tbl_rows)
            print(tbl_row)
            print(tbl_src)
            print(all_srcs)
            for src in all_srcs:
                tbl_row = [ src['name'] ]
                for use in all_uses:
                    tbl_row.append( read_sum_convert(results_file_reader, use['id'], src['id'], type=type) )
                tbl_src.append( tbl_row )
            print(tbl_src)
            print( tabulate( tbl_src, tablefmt=tablefmt, headers=headers, numalign=numalign, floatfmt=floatfmt ) )
            print("\n============================\n")
            
            header=tbl_src[0]
            rows=tbl_src[1:]
            with open('output.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header
                writer.writerows(rows)   # Write the data rows
                
                
            '''sankey=iesve.VESankey('depth')
            sankey.add_column_names(['electricity','Natural gas'])
            sankey.set_title('trail')
            
            sankey.add_node_columns({'electricity':0})
            sankey.add_node_columns({'light':1})
            sankey.add_connections([('electricity','light',2500)])
            sankey.generate_sankey()
            sankey.save_png('trails')'''
                
            
                
            df = pd.read_csv('output.csv')
            print(df)
            print(df.columns)
            import pandas as pd

            

            # Convert to DataFrame
            
            print(df)
            a=len(tbl_src)
            print( 'the value of a is ',a)
            # Define the sources and targets
            #sourcess=[]
            sources=[]
            ###TRYING TO DO SOMETHING FOR SOURCES
            for j in tbl_src:
                print(j)
                if j[0]!='kWh':
                    if j[0]!='Total':
                        sources.append(j[0])
            print(sources)        
                        
                    
              
            #sources = ['Electricity','Natural Gas']
            
            
            
            
            
       
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            targets=[]
            for i in tbl_rows:
                targets.append(i)
                
            

            # Initialize empty list for Sankey data
            sankey_data = []

            # Populate the Sankey data
            for source in sources:
                for target in targets:
                    if source == 'Total' or target == 'Total':
                        continue
                    value = df.loc[df['kWh'] == source, target].values[0]
                    if not pd.isna(value):
                        sankey_data.append({
                            'Source': source,
                            'Target': target,
                            'Value': value
                        })

            # Add flows to the 'Total' row
            '''for target in targets:
                value = df.loc[df['kWh'] == 'Total', target].values[0]
                if not pd.isna(value):
                    sankey_data.append({
                        'Source': target,
                        'Target': 'Total',
                        'Value': value
                    })'''
            # Convert to DataFrame
            sankey_df = pd.DataFrame(sankey_data)

            # Print the DataFrame to check
            print(sankey_df)
            
            
                        # Extract unique labels
            labels = pd.concat([sankey_df['Source'], sankey_df['Target']]).unique()

            # Map labels to indices
            label_index = {label: idx for idx, label in enumerate(labels)}

            # Create Sankey diagram
            fig = go.Figure(go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels
                ),
                link=dict(
                    source=sankey_df['Source'].map(label_index).tolist(),
                    target=sankey_df['Target'].map(label_index).tolist(),
                    value=sankey_df['Value'].tolist()
                )
            ))

            # Update layout
            fig.update_layout(title_text="Energy Flow Sankey Diagram", font_size=10)
            fig.show()

            
        
        # Create Energy Use Matrix by Meter
        if show_meter_matrix is True:
            print("\n=== Energy Meter Matrix ===\n")
            tbl_met = []
            tbl_row = [ units ]
            for use in all_uses:
                tbl_row.append( use['name'] )
            tbl_met.append( tbl_row )
            for met in all_mets:
                tbl_row = [ "Total" if met['source_id'] is iesve.EnergySource.unspecified else map_srcs[ met['source_id'] ]['name'] ]
                if met['name'] is not "":
                    tbl_row[0] += ": " + met['name']
                for use in all_uses:
                    tbl_row.append( read_sum_convert(results_file_reader, use['id'], met['source_id'], met['id'], type, 0) ) # 0: don't add sub meters (so we're not double counting)
                tbl_met.append( tbl_row )
            print( tabulate( tbl_met, tablefmt=tablefmt, headers=headers, numalign=numalign, floatfmt=floatfmt ) )
            print("\n===========================\n")
            
            
        
        # Display Example Groupings
        if show_groupings is True:
            print("\n=== Example Groupings ===\n")
            # groups = { "name" : [ <uses>, <sources> ], ... }
            groups = {
                "Electricity" : [
                    None,
                    iesve.EnergySource.elec
                ],
                "Electricity Generation" : [
                    [
                        iesve.EnergyUse.prm_elec_gen_chp,
                        iesve.EnergyUse.prm_elec_gen_wind,
                        iesve.EnergyUse.prm_elec_gen_pv,
                    ],
                    iesve.EnergySource.grid_disp_elec
                ],
                "Fossil Fuels" : [
                    None,
                    [
                        iesve.EnergySource.nat_gas,
                        iesve.EnergySource.oil,
                        iesve.EnergySource.coal,
                    ]
                ],
                "Other Fuels" : [
                    None,
                    [
                        iesve.EnergySource.misc_a,
                        iesve.EnergySource.misc_b,
                        iesve.EnergySource.misc_c,
                        iesve.EnergySource.misc_d,
                        iesve.EnergySource.misc_e,
                        iesve.EnergySource.misc_f,
                        iesve.EnergySource.misc_g,
                        iesve.EnergySource.misc_h,
                        iesve.EnergySource.misc_i,
                        iesve.EnergySource.misc_j,
                        iesve.EnergySource.misc_k,
                        iesve.EnergySource.misc_l,
                        iesve.EnergySource.misc_m,
                        iesve.EnergySource.misc_n,
                        iesve.EnergySource.misc_o,
                        iesve.EnergySource.misc_p,
                        iesve.EnergySource.misc_q,
                        iesve.EnergySource.misc_r,
                        iesve.EnergySource.misc_s,
                        iesve.EnergySource.misc_t,
                        iesve.EnergySource.misc_u,
                        iesve.EnergySource.misc_v,
                        iesve.EnergySource.misc_w,
                        iesve.EnergySource.misc_x,
                        iesve.EnergySource.misc_y,
                        iesve.EnergySource.misc_z,
                    ]
                ],
                "Lighting" : [
                    [
                        iesve.EnergyUse.prm_interior_lighting,
                        iesve.EnergyUse.prm_exterior_lighting,
                    ],
                    None
                ],
            }
            total_val = 0
            for name,group in groups.items():
                aps_data = results_file_reader.get_energy_results_ex( group[0], group[1], type )
                group_val = sum_convert( results_file_reader, aps_data, type )
                total_val = total_val + group_val
                print( "%-30s %15.3f %s" % ( name, group_val, units ) )
            print( "\n%-30s %15.3f %s" % ( "Total", total_val, units ) )
            print("\n======================\n")
        
        # Close APS file:
        results_file_reader.close()
