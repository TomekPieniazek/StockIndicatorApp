package com.example.stocksignals.api

import retrofit2.Response
import retrofit2.http.GET

typealias SignalMap = Map<String, String>

interface SignalService {
    @GET("signals")
    suspend fun getSignals(): Response<SignalMap>
}
