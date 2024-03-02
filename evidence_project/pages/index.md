---
title: Monthly Crypto Recap
---

_Official monthly crypto recap made by [Coinpaprika](https://coinpaprika.com/)_


# Market overall 

## **₿itcoin Performance**

```sql btc_mo_end 
select 
  market_cap as marketcap, 
  close as price, 
  volume as volume
from 
  btc_data
order by date desc
limit 1
```

<BigValue 
    data={btc_mo_end} 
    value='marketcap' 
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>

<BigValue 
    data={btc_mo_end} 
    value='price'
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0'
/>


<BigValue 
    data={btc_mo_end} 
    value='volume' 
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>

```sql btc_price_data
select
  close as price, 
  volume as volume, 
  market_cap as marketcap, 
  date as date, 
  fee as fee
from 
  'btc_data'
```

### Price 

<Details title="Details">
    

    Bitcoin everyday's close price in US Dollars.

    *Data Source:*
    Coinpaprika API 

</Details>

<AreaChart 
  data={btc_price_data} 
  x=date
  y=price 
  colorPalette={['#DB822E']}
  yScale=true
  yFmt='$#,##0.0,"k"'
>
</AreaChart>

### Marketcap

<Details title="Details">
    
    What is marketcap?

    ### Marketcap   

    Market capitalization, or market cap, is a popular measure of a company's or cryptocurrency's total value in the market. It is calculated by multiplying the current market price per share or unit by the total number of outstanding shares or units. Market cap provides investors and analysts with insights into the size and relative importance of a company or cryptocurrency within the broader financial landscape. 

    *Calculation:*
    Asset's cirrculating supply * Bitcoin price in US Dollar

    *Source:*
    Coinpaprika API

</Details>


<LineChart
  data={btc_price_data}
  x=date
  y=marketcap
  colorPalette={['#DB822E']}
  yFmt='$#,##0,,,"B"'	
  yScale=true
>
</LineChart>

### Volume

<Details title="Details">
    
    What is volume?

    ### Volume   
    
    Volume refers to the total quantity of a specific cryptocurrency traded on exchanges within a given period.
    
    _Calculation:
    Volume (USD) = Number of Coins or Tokens Traded * Price of the Cryptocurrency in USD_

    *Source:*
    Coinpaprika API

</Details>

<BarChart
  data={btc_price_data}
  x=date
  y=volume
  colorPalette={['#DB822E']}
  yFmt='$#,##0.0,,,"B"'
>
</BarChart>

### Fee 
<Details title="Details">
    
    What is fee?

    ### Fee   
    

    Bitcoin fee, often referred to as transaction feee, are charges users pay to have their Bitcoin transactions processed and confirmed by miners on the Bitcoin network    
    
    _Calculations:_

    Fee (in satoshi) = Transaction Input Value (sat) - Transaction Output Value (sat)

    1 satoshi (sat.) = 0.00000001BTC

    *Source:*
    dune.com

</Details>

```sql btc_fee 
select 
  fee,
  date
from
  btc_data
```

<LineChart
  data={btc_fee}
  x=date
  y=fee
  colorPalette={['#DB822E']}
  yFmt='#,##0.0,"k"'
>
</LineChart>


### Liquidity

```sql btc_liq
select * 
from btc_liquidity_data
```

<Details title="Details">
    
    What is liquidity?

    ### Liquidity   

    Liquidity refers to the ease with which an asset can be bought or sold in the market without causing a significant impact on its price. High liquidity means there are a sufficient number of buyers and sellers in the market, making it easy to execute trades quickly at stable prices. On the other hand, low liquidity may result in larger price swings and higher transaction costs.

    For our calculations we are considering only markets to stablecoins.

    Bids >> Buy orders 
    
    Asks >> Sell orders
 
    *Calculation:*


    *Source:*
    Coinpaprika API

</Details>


<LineChart
    data={btc_liq} 
    x=time 
    y={["asks","bids","combined_orders"]}
    xAxisTitle=true 
    yAxisTitle=true
    colorPalette={['#983C2D','#E2AC48','#B96028']}
/>


```sql bitcoin_active_addresses 
select 
  active_addresses
from 
  'active_addresses'
where 
  name = 'bitcoin'
```

### Active addresses 

Last month, there were **<Value data={bitcoin_active_addresses} fmt=0/>** Bitcoin addresses with at least one transaction.

---


## **Ethereum Performance**

```sql eth_mo_end 
select 
  market_cap as marketcap, 
  close as price, 
  volume as volume
from 
  eth_data
order by date desc
limit 1
```

<BigValue 
    data={eth_mo_end} 
    value='marketcap' 
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>

<BigValue 
    data={eth_mo_end} 
    value='price'
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0'
/>


<BigValue 
    data={eth_mo_end} 
    value='volume' 
    sparkline='date'
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>

```sql eth_price_data
select
  close as price, 
  volume as volume, 
  market_cap as marketcap, 
  date as date, 
  fee as fee
from 
  'eth_data'
```

### Price 

<Details title="Details">
    
    ### Daily Ethereum Price

    Ethereum everyday's close price in US Dollars.

    *Data Source:*
    Coinpaprika API 

</Details>

<AreaChart 
  data={eth_price_data} 
  x=date
  y=price 
  colorPalette={['#445ADB']}
  yScale=true
  yFmt='$#,##0.0,"k"'
>
</AreaChart>

### Marketcap

<Details title="Details">
    
    What is marketcap?

    ### Marketcap   

    Market capitalization, or market cap, is a popular measure of a company's or cryptocurrency's total value in the market. It is calculated by multiplying the current market price per share or unit by the total number of outstanding shares or units. Market cap provides investors and analysts with insights into the size and relative importance of a company or cryptocurrency within the broader financial landscape. 

    *Calculation:*
    Asset's cirrculating supply * Ethereum price in US Dollar

    *Source:*
    Coinpaprika API

</Details>

<LineChart
  data={eth_price_data}
  x=date
  y=marketcap
  colorPalette={['#445ADB']}
  yFmt='$#,##0,,,"B"'	
  yScale=true
>
</LineChart>

### Volume

<Details title="Details">
    
    What is volume?

    ### Volume   
    
    Volume refers to the total quantity of a specific cryptocurrency traded on exchanges within a given period.
    
    _Calculation:
    Volume (USD) = Number of Coins or Tokens Traded * Price of the Cryptocurrency in USD_

    *Source:*
    Coinpaprika API

</Details>

<BarChart
  data={eth_price_data}
  x=date
  y=volume
  colorPalette={['#445ADB']}
  yFmt='$#,##0.0,,,"B"'
>
</BarChart>

### Fee 
Average daily Ethereum transaction fee. (in Gwei)


<Details title="Details">
    
    What is fee?

    ### Fee   
    

    Ethereum fee, often referred to as transaction fee, are charges users pay to have their Etherum transactions processed and confirmed.

    
    _Calculations:_

    Fee (in Gwei) = gas price (WEI) * gas_used (WEI)

    1 gwei = 0.000000001ETH

    *Source:*
    dune.com

</Details>


<LineChart
  data={eth_price_data}
  x=date
  y=fee
  colorPalette={['#445ADB']}
  yFmt='#,##0.0,,"M"'
>
</LineChart>


### Liquidity 


<Details title="Details">
    
    What is liquidity?

    ### Liquidity   

    Liquidity refers to the ease with which an asset can be bought or sold in the market without causing a significant impact on its price. High liquidity means there are a sufficient number of buyers and sellers in the market, making it easy to execute trades quickly at stable prices. On the other hand, low liquidity may result in larger price swings and higher transaction costs.

    For our calculations we are considering only markets to stablecoins.

    Bids >> Buy orders 
    
    Asks >> Sell orders
 
    *Calculation:*


    *Source:*
    Coinpaprika API
</Details>




```sql eth_liq
select * 
from eth_liquidity_data
```


<LineChart
    data={eth_liq} 
    x=time 
    y={["asks","bids","combined_orders"]}
    xAxisTitle=true 
    yAxisTitle=true
    colorPalette={['#225A76', '#A7E7F6','#011126']}
/>


```sql ethereum_active_addresses 
select 
  active_addresses
from 
  'active_addresses'
where 
  name = 'ethereum'
```

### Active addresses 

Last month, there were **<Value data={ethereum_active_addresses} fmt=0/>** Ethereum addresses with at least one transaction.

---

## Biggest gainers

```sql biggest_gainers
select 
  new_coin_name as coin_name, 
  month_change as change
from 
  coins_and_returns
order by 
  month_change desc 
limit 10
```
### TOP 10 gainers this month (%)

List of top 10 monthly price gainers from TOP 200 cryptocurrencies measured by marketcap.

<BarChart 
  data={biggest_gainers}
  x=coin_name
  y=change
  swapXY=true 
  colorPalette={['#009E05']}
/>

```sql biggest_gainer_coin
select 
  new_coin_name as coin_name, 
  month_change as change
from 
  coins_and_returns
order by 
  month_change desc 
limit 1
```

Last month, best performing coin was **<Value data={biggest_gainer_coin} column=coin_name/>** which gained **<Value data={biggest_gainer_coin} column=change/>%**.

---

## Worst performing 

```sql biggest_losers
select 
  new_coin_name as coin_name, 
  month_change as change
from 
  coins_and_returns
order by 
  month_change asc 
limit 10
```
### TOP 10 losers this month (%)

List of top 10 monthly price losers from TOP 200 cryptocurrencies measured by marketcap.

<BarChart 
  data={biggest_losers}
  x=coin_name
  y=change
  swapXY=true 
  colorPalette={['#C22921']}
/>

```sql biggest_loser_coin
select 
  new_coin_name as coin_name, 
  month_change as change
from 
  coins_and_returns
order by 
  month_change asc 
limit 1
```

Last month, the worst performing coin was **<Value data={biggest_loser_coin} column=coin_name/>** which dumped **<Value data={biggest_loser_coin} column=change/>%**.


---

# Blockchains data

```sql blockchains_data_v_a
select 
  blockchain as blockchain, 
  total_volume as volume, 
  active_addresses as addresses
from 
  blockchain_tx_and_vol_data
where 
  active_addresses > 0
```

## Monthly volume / active addresses
<BubbleChart 
    data={blockchains_data_v_a} 
    x=volume
    y=addresses 
    series=blockchain
    size=volume
    xAxisTitle=true 
    yAxisTitle=true
    yLog=true
    colorPalette = {['#00FFFF', '#FF0000', '#008000', '#800080', '#FFA500', '#FFFF00', '#0000FF']}
/>

## Volume

```sql blockchains_data
select 
  blockchain as blockchain, 
  total_volume as volume, 
  active_addresses as addresses
from 
  blockchain_tx_and_vol_data
where active_addresses > 0
```


<Details title="Details">
    
    
    

    Sum of all transactions performed on specific chains.  

    *Source:*
    Dune API

</Details>

<BarChart 
    data={blockchains_data} 
    x=blockchain
    y=volume
    yFmt='$#,##0.0,,,"B"'
    swapXY=true
    colorPalette = {['#9B59B6']}
/>

## Active addresses

<Details title="Details">
    
    How it is being counted?

    ### Active addresses   

    If it comes to the active addresses, we are using this phrase for every single address to have sent and/or received at least one transaction in specific month. 

    *Source:*
    Dune API

</Details>

<BarChart 
    data={blockchains_data} 
    x=blockchain
    y=addresses
    yFmt='#,##0.00,,"M"'
    swapXY=true
    colorPalette = {['#9B59B6']}
/>

---

# Developers activity
Number of github commits for projects in the last month.


<Details title="Details">
    
    What are github commits?

    ### Github commits   

    GitHub commits are essentially records of changes made to a project's codebase. They represent individual updates or additions to the code by developers. When someone works on a software project, they make changes to the code to add new features, fix bugs, or improve existing functionality. Each of these changes is captured as a commit.

    Please note that we are currently not following those changes for every single existing projects. 

    *Source:*
    Coinpaprika API

</Details>

```sql commits
select * 
from project_commits_data
order by commits desc
limit 20
```

<BarChart 
    data={commits} 
    x=coin_name
    y=commits
    swapXY=true
    colorPalette = {['#21DCD7']}
/>

---

# Crypto Exchanges
Volume from 10 biggest CEX / DEX for last 30 days.


```sql dex_vol_sum
select sum(vol_30_day_usd) as "DEX Volume"
from dex_data
limit 10
``` 

<BigValue 
    data={cex_vol_sum} 
    value='CEX Volume' 
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>

<BigValue 
    data={dex_vol_sum} 
    value='DEX Volume' 
    maxWidth='10em'
    fmt='$#,##0.0,,,"B"'	
/>


## Centralized Exchanges

Total volume of 10 biggest crypto centralized exchanges.

```sql cex_vol_rank
select 
  name as 'name', 
  vol_30_day_usd as 'volume'
from 
  cex_data
order by vol_30_day_usd desc
limit 10
```

<BarChart
  data={cex_vol_rank}
  x=name
  y=volume
  colorPalette={['#042940']}
  yFmt='$#,##0.0,,,"B"'
  swapXY=true
>
</BarChart>

---

## Decentralized Exchanges

Total volume of 10 biggest crypto decentralized exchanges.

```sql dex_vol_rank
select 
  name as 'name', 
  vol_30_day_usd as 'volume'
from 
  dex_data
order by vol_30_day_usd desc
limit 10
```


<BarChart
  data={dex_vol_rank}
  x=name
  y=volume
  colorPalette={['#DBF227']}
  yFmt='$#,##0.0,,,"B"'
  swapXY=true
>
</BarChart>
