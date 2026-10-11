package org.barsides.potholepatrol;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {

    private final List<String> queue = new ArrayList<String>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final EditText street = (EditText) findViewById(R.id.street);
        final EditText depth = (EditText) findViewById(R.id.depth);
        final TextView queueView = (TextView) findViewById(R.id.queue);
        Button report = (Button) findViewById(R.id.report);

        queue.add("Liberty Ave & 40th St · 7 in · scheduled spring 2031");
        queue.add("Boulevard of the Allies · 11 in · \"under review\"");
        queue.add("Greenfield Bridge ramp · 4 in · lost the paperwork");
        queueView.setText(render());

        report.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String where = street.getText().toString().trim();
                String inches = depth.getText().toString().trim();
                if (where.isEmpty() || inches.isEmpty()) {
                    Toast.makeText(MainActivity.this, "Tell us where and how deep.", Toast.LENGTH_SHORT).show();
                    return;
                }
                queue.add(where + " · " + inches + " in · added to the back of the line");
                queueView.setText(render());
                street.setText("");
                depth.setText("");
            }
        });
    }

    private String render() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < queue.size(); i++) {
            sb.append(i + 1).append(". ").append(queue.get(i)).append('\n');
        }
        return sb.toString().trim();
    }
}
