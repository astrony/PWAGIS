<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.32.0-Lima" styleCategories="Symbology|Forms">
  <renderer-v2 symbollevels="0" referencescale="-1" forceraster="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol name="0" is_animated="0" alpha="1" clip_to_extent="1" force_rhr="0" type="line" frame_rate="10">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0" id="{7b851d7b-eb4a-4fbe-a2ee-3938f897dfed}">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="square"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="line_color" type="QString" value="125,139,143,255"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.26"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_end_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_end_unit" type="QString" value="MM"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="trim_distance_start_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="trim_distance_start_unit" type="QString" value="MM"/>
            <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="_collectionId">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="_createdAt">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="_createdBy">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="_updatedAt">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="_updatedBy">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="agency">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="func">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="ถนนสายหลัก (ทางหลวงแผ่นดิน)" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="ถนนสายรอง (ทางหลวงชนบท)" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="ถนน , ตรอก" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="ทางเดินเท้า" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="ถนนส่วนบุคคล" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="ทางด่วน (Express Way)" type="QString" value="6"/>
              </Option>
              <Option type="Map">
                <Option name="ทางยกระดับ (Toll Way)" type="QString" value="7"/>
              </Option>
              <Option type="Map">
                <Option name="อื่นๆ หรือไม่มีข้อมูล" type="QString" value="9"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="roadId">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="ถนนลาดยาง" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="ถนนคอนกรีต" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="ถนนลูกรัง" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="ถนนหินคลุก" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="อื่นๆ หรือไม่มีข้อมูล" type="QString" value="9"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="syncstage">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <editform tolerant="1">/Users/krittaporn/Documents/PWA/form_road.ui</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="_collectionId" editable="1"/>
    <field name="_createdAt" editable="1"/>
    <field name="_createdBy" editable="1"/>
    <field name="_updatedAt" editable="1"/>
    <field name="_updatedBy" editable="1"/>
    <field name="agency" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="func" editable="1"/>
    <field name="id" editable="1"/>
    <field name="name" editable="1"/>
    <field name="roadId" editable="1"/>
    <field name="syncstage" editable="1"/>
    <field name="type" editable="1"/>
    <field name="width" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="_collectionId" labelOnTop="0"/>
    <field name="_createdAt" labelOnTop="0"/>
    <field name="_createdBy" labelOnTop="0"/>
    <field name="_updatedAt" labelOnTop="0"/>
    <field name="_updatedBy" labelOnTop="0"/>
    <field name="agency" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="func" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="roadId" labelOnTop="0"/>
    <field name="syncstage" labelOnTop="0"/>
    <field name="type" labelOnTop="0"/>
    <field name="width" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="_collectionId" reuseLastValue="0"/>
    <field name="_createdAt" reuseLastValue="0"/>
    <field name="_createdBy" reuseLastValue="0"/>
    <field name="_updatedAt" reuseLastValue="0"/>
    <field name="_updatedBy" reuseLastValue="0"/>
    <field name="agency" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
    <field name="func" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="name" reuseLastValue="0"/>
    <field name="roadId" reuseLastValue="0"/>
    <field name="syncstage" reuseLastValue="0"/>
    <field name="type" reuseLastValue="0"/>
    <field name="width" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <layerGeometryType>1</layerGeometryType>
</qgis>
