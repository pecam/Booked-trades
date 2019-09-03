<template lang='html'>
	<div class="container">
        <div class="rows">
            <div class="col text-right">
                <b-button type="submit" variant="primary" :to="{name: 'NewTrade'}">New Trade</b-button>
            </div>
        </div>
		<div class="row">
			<div class="col text-left">
				<h2>Booked Trades</h2>
				<div class="col-md-12">
					<b-table striped hover :items="trades" :fields="fields">
					</b-table>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

// import validators from 'vue-form-generator'
import axios from 'axios'
import swal from 'sweetalert'
export default {
	data () {
		return {
			fields: [
				{ key: 'identifier', label: "ID" },
				{ key: 'sell_currency__code', label: "Sell CCY" },
				{ key: 'sell_amount', label: "Sell Amount" },
				{ key: 'buy_currency__code', label: "Buy CCY" },
				{ key: 'buy_amount', label: "Buy Amount" },
				{ key: 'rate', label: "Rate" },
				{ key: 'date_booked', label: "Date Booked"}
			],
			trades: [],
		}
	},
	methods: {
		getTrades(){
			const path = 'http://127.0.0.1:8000/api/v1/currency_list/'
			axios.get(path).then((response) => {
            this.trades = response.data.results
		})
		.catch((error) => {
			console.log(error)
			})
		}
				
	},
	created(){
		this.getTrades()
	}
}
</script>
