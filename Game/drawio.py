import random, string

def randomword(length):
    letters = string.ascii_lowercase+string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

class Element(object):
    
    def __init__(self,ename,**kwargs):
        self.ename = ename
        self.attributes = kwargs
        self.contents=[]
        self.drawio_fname=None
        
        if self.ename not in ["mxfile","root","mxGeometry","mxPoint"]:
            self.attributes["id"]=randomword(20)

    def __str__(self):
        
        S = "<" + self.ename
        for k,v in self.attributes.items():
            k=k.replace("_","")
            if isinstance(v,str):
                S += f' {k}="{v}"'
            else:
                S += f' {k}={v}'
                
                
                
        if self.contents:
            S += ">"


            for c in self.contents:
                S1='\n'.join(["  "+x for x in str(c).split("\n")])
                S += "\n"+S1            

            S+="\n"
            S+=f"</{self.ename}>"

            if self.ename not in ["mxfile","root","diagram","mxGraphModel"]:
                if 'id' in self.attributes:
                    S+=f" <!-- {self.attributes['id']} -->"
                    
        else:
            S+=f" />"
            
            
        return S
    
    
    def __iadd__(self,other):
        self.contents.append(other)
        return self


class drawio(object):
    
    def __init__(self,width,height):
        
        self.doc=Element("mxfile",
                    host="Electron",
                    modified="2024-02-12T18:26:55.201Z",
                    agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/22.1.18 Chrome/120.0.6099.199 Electron/28.1.2 Safari/537.36",
                    etag="ufVDfNkRy14tUbGhxmqu",
                    version="22.1.18",type="device",)
        
        self.page=Element("diagram",
                     name="Page-1",
                    )
        self.doc+=self.page


        self.model=Element("mxGraphModel",
                      dx="1114",
                      dy="894",
                      grid="1",
                      gridSize="10",
                      guides="1",
                      tooltips="1",
                      connect="1",
                      arrows="1",
                      fold="1",
                      page="1",
                      pageScale="1",
                      pageWidth=str(width),
                      pageHeight=str(height),
                      math="0",
                      shadow="0")
        self.page+=self.model
        self.root=Element("root")
        self.model+=self.root

        self.root+="""
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        """.strip()

    def text(self,x,y,text,fontsize=None,align='left',verticalAlign='bottom',bold=False,italic=False):
        
        if not fontsize is None:
            value=f"&lt;font style=&quot;font-size: {fontsize}px;&quot;&gt;{text}&lt;/font&gt;"
        else:
            value=text
            fontsize=12


        if bold:
            value=f"&lt;b&gt;{text}&lt;/b&gt;"
        if italic:
            value=f"&lt;i&gt;{text}&lt;/i&gt;"
        
        cell=Element("mxCell",
                    value=value,
                    style=f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign={verticalAlign};whiteSpace=wrap;rounded=0;",
                    vertex="1",
                    parent="1")

        width=fontsize*len(text)
        height=2*fontsize
        cell+=Element("mxGeometry",x=str(x),y=str(y-height),width=str(width),height=str(height),_as="geometry")
        self.root+=cell
        
    def line(self,x1,y1,x2,y2,strokeColor="#000000"):
        cell=Element("mxCell",
                    value="",
                    style=f"endArrow=none;html=1;rounded=0;strokeColor={strokeColor};",
                    edge="1",
                    parent="1")
        geometry=Element("mxGeometry",width="50",height="50",relative="1",_as="geometry")
        geometry+=Element("mxPoint",x=str(x1),y=str(y1),as_="sourcePoint")
        geometry+=Element("mxPoint",x=str(x2),y=str(y2),as_="targetPoint")

        cell+=geometry
        self.root+=cell
        

        # <mxCell id="moGaSVdySe5eVO_UJH3o-68" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#dae8fc;gradientColor=#7ea6e0;strokeColor=#6c8ebf;" parent="1" vertex="1">
        #   <mxGeometry x="40" y="240" width="40" height="40" as="geometry" />
        # </mxCell>

    def circle(self,x,y,radius,
                text="",fontsize=None,
                fillColor="#FFFFFF",strokeColor="#000000",fillOpacity="100"):
        if not fontsize is None:
            value=f"&lt;font style=&quot;font-size: {fontsize}px;&quot;&gt;{text}&lt;/font&gt;"
        else:
            value=text
            fontsize=12

        cell=Element("mxCell",
                    value=value,
                    style=f"ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={fillColor};strokeColor={strokeColor};fillOpacity={fillOpacity};",
                    vertex="1",
                    parent="1")
        cell+=Element("mxGeometry",x=str(x-radius),y=str(y-radius),width=str(2*radius),height=str(2*radius),_as="geometry")
        self.root+=cell
        

    def rectangle(self,x,y,width,height,text="",fontsize=None,
                 fillColor="#FFFFFF",strokeColor="#000000",fillOpacity="100",rounded=True):
                
        rounded=int(rounded)
        if not fontsize is None:
            value=f"&lt;font style=&quot;font-size: {fontsize}px;&quot;&gt;{text}&lt;/font&gt;"
        else:
            value=text
            fontsize=12
        
        cell=Element("mxCell",
                    value=value,
                    style=f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fillColor};strokeColor={strokeColor};fillOpacity={fillOpacity};",
                    vertex="1",
                    parent="1")
        cell+=Element("mxGeometry",x=str(x),y=str(y),width=str(width),height=str(height),_as="geometry")
        self.root+=cell
        
        
        
    def __iadd__(self,other):
        self.root+=other
        return self
    
    
    def save(self,filename,verbose=False):
        import os

        base,ext=os.path.splitext(filename)

        newfname=base+".drawio"
        self.drawio_fname=newfname


        if verbose:
            print(f"Saving {newfname}...",end="")

        with open(newfname,"w") as f:
            f.write(str(self.doc))

        if verbose:
            print("done.")

        if ext=='.drawio':
            return

        cmd=f'/Applications/draw.io.app/Contents/MacOS/draw.io --export --format {ext[1:]} --crop --transparent "{newfname}" "{filename}"'
        if verbose:
            print(cmd)
        os.system(cmd)
            
    