from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone


register = template.Library()

TABLE_HEAD = '''
<table class="table">
  <tbody>
'''

TABLE_TAIL = '''
  </tbody>
</table>
'''

TABLE_CONTENT = '''
    <tr>
      <td>{name}</td>
      <td>{value}</td>
    </tr>
'''

PRODUCT_SPEC = {
    'notebook':{
        'Diagonal': 'diagonal',
        'Type of Display': 'display_type',
        'Processor Freq': 'processor_freq',
        'Ram': 'ram',
        'Battery': 'time_without_charge',
        'Price': 'price'
    },
    'smartphone':{
        'Diagonal': 'diagonal',
        'Type of Display': 'display_type',
        'Display pixel': 'resolution',
        'Battery': 'accum_volume',
        'Ram': 'ram',
        'SD': 'sd',
        'SD max volume': 'sd_volume_max',
        'Main Camera': 'main_cam_mp',
        'Front Camera': 'frontal_cam_mp'

    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value = getattr(product, value))

    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            #PRODUCT_SPEC['smartphone'].pop('SD max volume')
            PRODUCT_SPEC['smartphone']['SD max volume'] = 'sd_volume_max'
            print('Hello')
        else:
            PRODUCT_SPEC['smartphone']['SD max volume'] = 'sd_volume_max'
            print('NOO')
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)