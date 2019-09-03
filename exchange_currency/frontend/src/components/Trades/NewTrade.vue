<template lang='html'>
	<div class="container">
		<div class="row">
			<div class="col">
				<h1>New Trade</h1>
				<div class="card">
					<div class="card-body">
						<form @submit="onSubmit">
							<div class="form-group row">
								<label for="sell_currency" class="col-sm-2 col-form-label">Sell currency </label>
								<div class="col-sm-2">
									<select name="sell_currency" v-model="sell_currency" @change="calculateRate">
										<option disabled value="">Select one</option>
										<option>USD</option>
										<option>EUR</option>
										<option>GBP</option>
									</select>
								</div>

								<label for="rate" class="col-sm-2 col-form-label">Rate </label>
								<div class="col-sm-2">
									<input type="number" name="rate" class="form-control" v-model="rate" readonly="True">
								</div>

								<label for="buy_currency" class="col-sm-2 col-form-label">Buy currency </label>
								<div class="col-sm-2">
									<select name="buy_currency" v-model="buy_currency" @change="calculateRate">
										<option disabled value="">Select one</option>
										<option>USD</option>
										<option>EUR</option>
										<option>GBP</option>
									</select>
								</div>
							</div>
							<div class="form-group row">
								<label for="sell_amount" class="col-sm-3 col-form-label">Sell amount </label>
								<div class="col-sm-3">
									<input type="number" name="sell_amount" class="form-control" v-model="sell_amount" @change="calculateBuyAmount">
								</div>
								<label for="buy_amount" class="col-sm-3 col-form-label">Buy amount </label>
								<div class="col-sm-3">
									<input type="number" name="buy_amount" class="form-control" v-model="buy_amount" readonly="True">
								</div>
							</div>
							<br>
							<div class="rows">
								<div class="col text-left">
									<b-button type="submit" v-on:click="submit">Create</b-button>
									<b-button type="submit" :to="{name: 'ListTrades'}">Cancel</b-button>
								</div>
							</div>
						</form>
					</div>
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
			sell_currency: '',
			buy_currency: '',
			rate: 0,
			sell_amount: 0,
			buy_amount: 0,
		}
	},
	methods: {
		onSubmit(event){
			event.preventDefault()
			const sell_currency = this.sell_currency
			const buy_currency = this.buy_currency
			const sell_amount = this.sell_amount
			const rate = this.rate
			const buy_amount = this.buy_amount

			const path = 'http://127.0.0.1:8000/api/v1/new_trade/' + sell_currency + '/' + sell_amount + '/' + buy_currency + '/' + buy_amount + '/' + rate
			axios.put(path, this.model).then((response) => {
				swal("New trade create sucessfully", "", "success")
				// location.href = '/'
			})
			.catch((response) => {
				swal("Sorry, there is a problem with the element!", "", "error")
			})
		},
		calculateRate(event){
			const sell_currency = this.sell_currency
			const buy_currency = this.buy_currency
			if (sell_currency && buy_currency) {
				const path = 'http://127.0.0.1:8000/api/v1/get_rate/?base=' + sell_currency + '&symbols=' + buy_currency
                axios.get(path).then((response) => {
                	if (response.data.success == true){
                		this.rate = response.data.rates
                	}else{
                		swal(response.data.error + '. Please change currency.')
                	}
                })
                .catch((response) => {
                	swal(response.data.error)
                }) 
				
			}

		},
		calculateBuyAmount(event){
			const buy_amount = this.sell_amount * this.rate
			this.buy_amount = buy_amount.toFixed(2);
		},
	},
	created () {
	},
}
</script>
<style lang="css" scoped>
</style>