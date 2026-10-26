package com.fal.fal4mir;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Button;
import android.widget.ScrollView;
import androidx.appcompat.app.AppCompatActivity;
import com.bumptech.glide.Glide;
import com.fal.fal4mir.data.FalApi;

public class MainActivity extends AppCompatActivity {
    private TextView numberView, ghazalView, tabirView;
    private ImageView imageView;
    private Button refreshBtn, voiceBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        numberView = findViewById(R.id.number);
        ghazalView = findViewById(R.id.ghazal);
        tabirView = findViewById(R.id.tabir);
        imageView = findViewById(R.id.image);
        refreshBtn = findViewById(R.id.refresh_btn);
        voiceBtn = findViewById(R.id.voice_btn);

        refreshBtn.setOnClickListener(v -> refresh());
        voiceBtn.setOnClickListener(v -> playVoice());

        refresh();
    }

    private void refresh() {
        new Thread(() -> {
            FalApi.FalData fal = FalApi.fetch();
            runOnUiThread(() -> {
                if (fal != null) {
                    numberView.setText(fal.number);
                    ghazalView.setText(fal.ghazal);
                    tabirView.setText(fal.tabir);
                    if (!fal.imageUrl.isEmpty()) {
                        Glide.with(this).load(fal.imageUrl).into(imageView);
                    }
                }
            });
        }).start();
    }

    private void playVoice() {
        // Voice playback would go here
    }
}
