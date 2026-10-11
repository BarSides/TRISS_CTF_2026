package org.barsides.parkingchair;

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
        final TextView status = (TextView) findViewById(R.id.status);
        final TextView result = (TextView) findViewById(R.id.result);
        Button move = (Button) findViewById(R.id.move);

        move.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String entered = code.getText().toString();
                if (ChairLock.isOwner(entered)) {
                    status.setText("Chair is UP. Spot released to the owner.");
                    result.setTextColor(getColor(R.color.gold));
                    result.setText(ChairLock.ownerReceipt());
                } else {
                    result.setTextColor(getColor(R.color.danger));
                    result.setText(R.string.wrong_code);
                }
            }
        });
    }
}
