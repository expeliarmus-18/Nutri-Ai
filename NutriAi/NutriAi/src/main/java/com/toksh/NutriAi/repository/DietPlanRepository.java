package com.toksh.NutriAi.repository;

import com.toksh.NutriAi.entt.DietPlan;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface DietPlanRepository extends MongoRepository<DietPlan, ObjectId> {
    DietPlan findByEmail(String email);
}