import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ListTrades from '@/components/Trades/ListTrades'
import NewTrade from '@/components/Trades/NewTrade'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ListTrades',
      component: ListTrades
    },
    {
      path: '/new',
      name: 'NewTrade',
      component: NewTrade
    },
  ],
  mode: 'history'
})
