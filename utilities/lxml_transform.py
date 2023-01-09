from lxml import etree
import argparse

xslt_root = etree.XML('''
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output omit-xml-declaration="yes" indent="yes"/>
 <xsl:strip-space elements="*"/>

 <xsl:template match="node()|@*">
     <xsl:copy>
       <xsl:apply-templates select="node()|@*"/>
     </xsl:copy>
 </xsl:template>

 <xsl:template match=
    "*[not(@*|*|comment()|processing-instruction())
     and normalize-space()=''
      ]"/>
</xsl:stylesheet>
''')

transform = etree.XSLT(xslt_root)
parser = argparse.ArgumentParser(description='Crawl Papers and Generate Output XML.')
parser.add_argument("-i", "--input", dest="input", help="Specify input XML file.", required=True)
parser.add_argument("-o", "--output", dest="output", help="Specify output XML file.", required=True)
args = parser.parse_args()
xml = etree.parse(args.input)
results = transform(xml)
xml_string = etree.tostring(results, pretty_print=True, encoding='iso-8859-1')
with open(args.output, 'wb') as my_xml:
    my_xml.write(xml_string)