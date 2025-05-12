package com.example.stocksignals

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.stocksignals.ui.theme.StockSignalsTheme
import com.example.stocksignals.viewmodel.SignalViewModel
import com.example.stocksignals.viewmodel.UiState

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            StockSignalsTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    SignalScreen()
                }
            }
        }
    }
}

@Composable
fun SignalScreen(vm: SignalViewModel = viewModel()) {
    val state by vm.uiState.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Button(onClick = { vm.fetchSignals() }) {
            Text("Fetch Signals")
        }
        Spacer(modifier = Modifier.height(24.dp))

        when (state) {
            is UiState.Idle -> Text("Tap the button to load signals.")
            is UiState.Loading -> Text("Loading...")
            is UiState.Error -> Text((state as UiState.Error).message, color = MaterialTheme.colorScheme.error)
            is UiState.Success -> SignalList((state as UiState.Success).data)
        }
    }
}

@Composable
fun SignalList(signals: Map<String,String>) {
    LazyColumn(
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        items(signals.toList()) { (ticker, signal) ->
            SignalCard(ticker, signal)
        }
    }
}

@Composable
fun SignalCard(ticker: String, signal: String) {
    val color = when(signal.uppercase()) {
        "BUY" -> MaterialTheme.colorScheme.primary
        "SELL" -> MaterialTheme.colorScheme.error
        else -> MaterialTheme.colorScheme.onSurfaceVariant
    }
    Card(
        colors = CardDefaults.cardColors(containerColor = color.copy(alpha = 0.1f)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(ticker, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(signal, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        }
    }
}
