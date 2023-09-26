import { ElNotification } from 'element-plus'
import { h } from 'vue'

export const notify = (type: notifyType, message: string, title?: string) => {
  ElNotification({
    title,
    type,
    message: h('i', { style: 'color: teal' }, message),
    duration: 2000,
  })
}
