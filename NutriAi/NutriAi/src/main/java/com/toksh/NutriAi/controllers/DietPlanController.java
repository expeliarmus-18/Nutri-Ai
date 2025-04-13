package com.toksh.NutriAi.controllers;


import com.toksh.NutriAi.entt.DietPlan;
import com.toksh.NutriAi.entt.User;
import com.toksh.NutriAi.repository.DietPlanRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/api/diet")
public class DietPlanController {


    @Value("${python.ai.url}")
    private String pythonAiUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @Autowired
    private DietPlanRepository dietPlanRepository;

    @PostMapping("/generate")
    public ResponseEntity<?> generateAndSaveDietPlan(@RequestBody User user) {
        try {
            // Prepare JSON request with headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<User> requestEntity = new HttpEntity<>(user, headers);

            // Send POST request to Flask API
            ResponseEntity<Map> response = restTemplate.exchange(
                    pythonAiUrl, HttpMethod.POST, requestEntity, Map.class
            );

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                DietPlan dietPlan = new DietPlan();
                dietPlan.setEmail(user.getEmail());
                dietPlan.setPlan(response.getBody());

                return ResponseEntity.ok(dietPlanRepository.save(dietPlan));
            } else {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                        .body("Failed to generate diet plan");
            }

        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }
    }

    @GetMapping("/{email}")
    public ResponseEntity<?> getDietPlan(@PathVariable String email) {
        DietPlan plan = dietPlanRepository.findByEmail(email);
        if (plan != null) {
            return ResponseEntity.ok(plan);
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Diet plan not found");
    }
}

