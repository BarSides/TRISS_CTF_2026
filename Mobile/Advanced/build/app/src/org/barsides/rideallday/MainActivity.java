package org.barsides.rideallday;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final EditText code = (EditText) findViewById(R.id.code);
        final TextView result = (TextView) findViewById(R.id.result);
        Button scan = (Button) findViewById(R.id.scan);

        scan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // A genuine wristband code is the flag itself.
                if (Gate.scan(code.getText().toString())) {
                    result.setTextColor(getColor(R.color.gold));
                    result.setText(R.string.ok);
                } else {
                    result.setTextColor(getColor(R.color.danger));
                    result.setText(R.string.bad);
                }
            }
        });
    }
}
