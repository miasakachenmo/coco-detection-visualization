<template>
  <el-container style="height: 100%;">
    <el-main>
      <el-row >

        <!-- left(items) -->
        <el-col :span="4">
          <div class="grid-up" :style="style" >
            <div v-for="annotation in annotations"   >
              <div class="noselect" :id="annotation.id" @mouseenter="anno_mouse_enter($event,annotation)" @mouseout="anno_mouse_out($event,annotation)">
                {{annotation.score.toFixed(7)}}:{{annotation.category_id}}:{{catid_to_catname[annotation.category_id-1].name}}
              </div>
              <!-- {{annotation.score}} -->
            </div>
          </div>
        </el-col>


        <!-- mid(graph) (put a canvas here)-->
        <el-col :span="16">
          <div id="cvs_father" class="grid-up-mid" :style="style"  >
            <canvas id="cvs" @mouseenter="draw_image();draw_annotations(annotations)" @click="click_canvas" > </canvas>
          </div>
        </el-col>

        <!-- right -->
        <el-col :span="4">
          <div class="grid-up"   >

            
            <el-row  style="width: 100%; ">
              <el-col :span="12"  style="padding-right: 5px;" >
                <el-button type="primary" @click="last"  style="  width: 100%;" >Last</el-button>
              </el-col>
              <el-col :span="12" style="padding-left: 5px;">
                <el-button type="primary" @click="next" style=" width: 100%;" >Next</el-button>
              </el-col>
            </el-row>

            <el-row  style="width: 100%; ">
              <el-col :span="20" >
                <el-input v-model="input" @keyup.enter.native="refresh()" placeholder="Image id" />
              </el-col>
              <el-col :span="4" >
                <el-button type="primary" @click="refresh" style=" width: 100%;" >Go</el-button>
              </el-col>
            </el-row>

            <el-row  style="width: 100%; ">
              <el-col :span="8"  style="padding-right: 3px;" >
                <el-button type="danger" @click="annotation_color='rgba(255,0,0,1)';refresh()"  style="  width: 100%;" >Red</el-button>
              </el-col>
              <el-col :span="8" style="padding-left: 3px;">
                <el-button type="success" @click="annotation_color='rgba(0,255,0,1)';refresh()" style=" width: 100%;" >Green</el-button>
              </el-col>
              <el-col :span="8" style="padding-left: 3px;">
                <el-button type="primary" @click="annotation_color='rgba(0,0,255,1)';refresh()" style=" width: 100%;" >Blue</el-button>
              </el-col>
            </el-row>
            <el-row>
              TIPS:点击图中的框可以选中包含鼠标的所有框
            </el-row>

            <div v-for="json_name in json_names" >
                <el-popover
                    class="el-row"
                    placement="left"
                    trigger="hover"
                    width="400px"
                    :content="json_name[0]">
                    <template #reference>
                      <el-button :type="json_name[1]?'primary':'default'" @click="choose_file(json_name[0])"  style=" width:100%; " >{{ellipsis(json_name[0])}}</el-button>
                    </template>          
                </el-popover>  
              <!-- <el-button>{{json_name}}</el-button> -->
            </div>
          </div>
        </el-col>


      </el-row>
      <el-row>
        <!-- <el-col :span="24"> -->
          <div class="grid-down" >
            <el-col class="noselect" v-for="annotation in selected_annotations" style=" border:2px solid #000;margin-left: 2px;">
                <div  @mouseenter="anno_mouse_enter($event,annotation)" @mouseout="anno_mouse_out($event,annotation)" > 
                  {{annotation.score.toFixed(7)}}:{{annotation.category_id}}:{{catid_to_catname[annotation.category_id-1].name}}
                </div>
            </el-col>
            
          </div>
        <!-- </el-col> -->
      </el-row>
    </el-main>

  </el-container>

</template>
<script>
import axios from 'axios' 
import { getCurrentInstance } from 'vue';
// json_activate={}
// g=getCurrentInstance()
var boxes=[]
var canvas;
var ctx;

const app= {
    setup(){
      // const _instance = getCurrentInstance();
      // const vueInstance = _instance.appContext;
    },
    data() {
      return {
        json_names:[],
        //本张图的annotations
        annotations:[],
        selected_annotations:[],
        img_dict:null,
        img:null,
        json_now:"",
        input:"1",
        upper_height:600,
        factor:1,
        catid_to_catname:{},
        annotation_color:"rgba(255,0,0,1)",
        backend_url:"http://127.0.0.1:5000/"

        // json_activate:{},
      }
    },
    mounted() {
      console.log(`the component is now mounted.`)
      console.log(axios)
      canvas=document.getElementById('cvs')
      ctx=canvas.getContext("2d")
      axios.get(this.backend_url+"getcategories").then(
        res=>{
          // console.log(res)
          this.catid_to_catname=res.data
          console.log(this.catid_to_catname)
          // for(let i=0;i<res.data.length;i++)
          // {
          //   this.json_names.push([res.data[i],false])
          // }
        }
      )
      axios.get(this.backend_url+"getnames").then(
        res=>{
          // console.log(res)
          for(let i=0;i<res.data.length;i++)
          {
            this.json_names.push([res.data[i],false])
          }
          this.json_now=this.json_names[0][0]
          this.json_names[0][1]=true
          this.$forceUpdate()
          this.refresh()
        }
      )
      
    },
  emits:{
  },
  methods:{
    last(){
      // console.log("last ")
      this.input=(parseInt(this.input)-1).toString()
      this.refresh()
    },
    next(){
      this.input=(parseInt(this.input)+1).toString()
      this.refresh()
    },
    ellipsis(value) {
            if (!value) return ''
            if (value.length > 30) {
                return value.slice(0,30) + '....'
            }
            return value
    },
    choose_file(name){
      // console.log(name)
      this.json_now=name
      // console.log(this)
      // console.log(app.data.json_names)
      // console.log(app.$data.json_names)
      for(let i=0;i<this.json_names.length;i++)
      {
        this.json_names[i][1]=false
        if (this.json_names[i][0]==name)
        {
          this.json_names[i][1]=true
        }
      }
      // json_activate[name]=true
      // console.log(name)
      // console.log("testa")
      this.$forceUpdate()
      this.refresh()
      return true
    },
    refresh(){
      axios.post(this.backend_url+"getannos",
                  {
                    'name':this.json_now,
                    'img_id':this.input
                  }).then(
                    res=>{
                      // console.log(res)
                      this.annotations=res.data
                    }
                  )
      axios.post(this.backend_url+"getimg",
                  {
                    'name':this.json_now,
                    'img_id':this.input
                  }).then(
                    res=>{
                      // console.log(res)
                      this.img_dict=res.data
                      // console.log(this.img_dict)
                      // this.annotations=res.data
                      this.draw_image(true)
                    }
                  )
      
      
    },

    anno_mouse_enter(e,annotation){

      // console.log(e)
      e.srcElement.style.backgroundColor="yellow"
      // console.log(annotation)
      this.draw_image()
      // console.log([annotation])
      this.draw_annotations([annotation])

    },
    anno_mouse_out(e,annotation){
      // console.log(e)
      e.srcElement.style.backgroundColor=""
      // console.log(annotation)
    },
    draw_image(refresh=false)
    {
      // var canvas = document.getElementById('cvs')
      var cvs_father=document.getElementById('cvs_father')
      var max_height=  parseInt(window.getComputedStyle(cvs_father).height.slice(0,-2))
      // console.log(cvs_father)
      var max_width=parseInt(window.getComputedStyle(cvs_father).width.slice(0,-2))
      // console.log("drawing")
      if (refresh)
      {

        var w_factor=this.img_dict.width/max_width
        var h_factor=this.img_dict.height/max_height
        // console.log(max_height)
        // var scaled_height=1
        // var scaled_width=1
        // var factor=1
        if(w_factor<=1&&h_factor<=1)
        {
          this.factor=1
        }
        else{
          this.factor=Math.max(w_factor,h_factor)
        }
      }

      let scaled_height=Math.floor(this.img_dict.height/this.factor)
      let scaled_width=Math.floor(this.img_dict.width/this.factor)
      // var ctx = canvas.getContext("2d")
      
      console.log(scaled_height)
      // console.log(scaled_width)
      canvas.height=scaled_height
      canvas.width=scaled_width
      // console.log(ctx)

      ctx.clearRect(0, 0,max_width,max_height);
      if(refresh)
      {
        this.img = new Image()
        // console.log(this.img_dict.img)
        var that=this
        this.img.onload=function(){
          // ctx.scale(1/factor,1/factor)
          // ctx.drawImage(img, 0, 0,that.img_dict.width,that.img_dict.height)
          ctx.drawImage(that.img, 0, 0,that.img_dict.width,that.img_dict.height,0,0,scaled_width,scaled_height)
          that.draw_annotations(that.annotations)
          // that.draw_annotations(that.annotations)
        };
        this.img.src =this.img_dict['img']
      }
      else{
        ctx.drawImage(this.img, 0, 0,this.img_dict.width,this.img_dict.height,0,0,scaled_width,scaled_height)
      }

    },
  //factor是为了配合图片的缩放尺度
  draw_annotations(annotations)
  {
    boxes=[]
    console.log("drawing annotation")
    var factor=this.factor
    // console.log(factor)
    ctx.strokeStyle=this.annotation_color;
    for(let i=0;i<annotations.length;i++)
    {
      let item=annotations[i]
      // console.log(item)
      let bbox=item.bbox
      let x=Math.floor(bbox[0]/factor)
      let y=Math.floor(bbox[1]/factor)
      let w=Math.floor(bbox[2]/factor)
      let h=Math.floor(bbox[3]/factor)
      ctx.strokeRect(x,y,w,h)
      var path = new Path2D();
      path.rect(x, y, w, h);
      boxes.push([item,path])
    }
  },
  click_canvas(e){
    this.selected_annotations=[]
    for (var i = 0; i < boxes.length; i++) {
        let box = boxes[i];
        if (ctx.isPointInPath(box[1], e.offsetX, e.offsetY)) {
          console.log("box " + (i + 1) + " clicked");
          this.selected_annotations.push(box[0])
        }
    }
  }
  },
  computed: {
    style () {
      return {
        height: `${this.upper_height}px`,
        // position: 'relative'
      }
    }
  }

}
// var json_activate={}
export default app;




</script>

<style>
@import './assets/base.css';

#app {
  /* max-width: 1280px; */
  margin: 0 auto;
  padding: 0rem;
  font-weight: normal;
}


.noselect {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
.el-row {
  margin-bottom: 4px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-up {
  border-radius: 4px;
  /* min-height: 600px;
  max-height: 600px; */
  overflow:auto;
}
.grid-up-mid {
  border-radius: 4px;
  /* min-height: 600px;
  max-height: 600px; */
  /* overflow:auto; */
}

.grid-down{
  border-radius: 4px;
  height: 100px;
  /* min-height: 200px; */
  /* flex-wrap: wrap; */
}

</style>
