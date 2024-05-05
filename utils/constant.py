

LABEL_COLOR = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'purple',
    5: 'cyan',
    6: 'magenta',
    7: 'yellow',
    8: 'lime',
    9: 'pink',
    10: 'teal'
}

WEIGHT_CHOICE = ["total_sale", "product_count","order_count","total_discount", "average_order_sale"]

def popup_html_item(latitude,
               longitude,
               labels,
               state_province_name,
               product_count,
               average_order_sale, 
               total_sale, 
               order_count, 
               total_discount):

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(state_province_name) + """
</head>
    <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Product Count</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(product_count) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Average Order Sale</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(average_order_sale) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Total Sale</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(total_sale) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Order Count</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(order_count) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Total Discount</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(total_discount) + """
</tr>
</tbody>
</table>
"""
    return html

def popup_html_item(latitude,
               longitude,
               labels,
               state_province_name,
               product_count,
               average_order_sale, 
               total_sale, 
               order_count, 
               total_discount):

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(state_province_name) + """
</head>
    <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Product Count</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(product_count) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Average Order Sale</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(average_order_sale) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Total Sale</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(total_sale) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Order Count</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(order_count) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Total Discount</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(total_discount) + """
</tr>
</tbody>
</table>
"""
    return html