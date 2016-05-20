VOLUME_XML="""
<disk type='network' device='disk'>
<source protocol='rbd' name='%s/%s'>
<host name='%s' port='5000'/>
</source>
<target dev='%s' bus='scsi'/>
</disk>"""





