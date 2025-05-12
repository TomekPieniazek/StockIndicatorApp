package com.example.stocksignals.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.stocksignals.api.RetrofitClient
import com.example.stocksignals.api.SignalService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed interface UiState {
    object Idle: UiState
    object Loading: UiState
    data class Success(val data: Map<String,String>): UiState
    data class Error(val message: String): UiState
}

class SignalViewModel: ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Idle)
    val uiState = _uiState.asStateFlow()

    private val service: SignalService by lazy {
        RetrofitClient.retrofit.create(SignalService::class.java)
    }

    fun fetchSignals() {
        _uiState.value = UiState.Loading
        viewModelScope.launch {
            try {
                val response = service.getSignals()
                if (response.isSuccessful) {
                    _uiState.value = UiState.Success(response.body() ?: emptyMap())
                } else {
                    _uiState.value = UiState.Error("HTTP ${'$'}{response.code()}")
                }
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.localizedMessage ?: "Unknown error")
            }
        }
    }
}
